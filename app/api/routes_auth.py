from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.db.models.user_db import UserDB
from app.schemas.user_schemas import UserCreate, UserLogin
import uuid
import resend
from passlib.context import CryptContext
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

# Configurar Resend
resend.api_key = "re_2YAK6sGa_9oeoMpAowbDTYGBRprR3xkXi"

# Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------
# REGISTRO
# ---------------------------------------------------------
@router.post("/register")
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(user_in.password)
    verification_token = str(uuid.uuid4())

    new_user = UserDB(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hashed_password,
        is_active=False,
        verification_token=verification_token
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verify_link = f"{settings.BACKEND_URL}/auth/verify/{verification_token}"

    resend.Emails.send({
        "from": "ManuPilot Trail <onboarding@resend.dev>",
        "to": user_in.email,
        "subject": "Verifica tu cuenta",
        "html": f"""
            <h2>Bienvenido a ManuPilot Trail</h2>
            <p>Pulsa el siguiente enlace para verificar tu cuenta:</p>
            <a href="{verify_link}">{verify_link}</a>
        """
    })

    return {"status": "ok", "message": "Usuario registrado. Verifica tu email."}


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@router.post("/login")
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == user_in.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta no verificada. Revisa tu correo.")

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return {"status": "ok", "user_id": user.id}


# ---------------------------------------------------------
# VERIFICAR TOKEN
# ---------------------------------------------------------
@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Token inválido")

    user.is_active = True
    user.verification_token = None
    db.commit()

    return {"status": "ok", "message": "Cuenta verificada"}


# ---------------------------------------------------------
# CHECK VERIFICACIÓN
# ---------------------------------------------------------
@router.get("/check-verified")
def check_verified(email: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Cuenta no verificada")

    return {"status": "verified"}


# ---------------------------------------------------------
# RECUPERAR CONTRASEÑA (ENVÍA EMAIL)
# ---------------------------------------------------------

class RecoverPasswordRequest(BaseModel):
    email: str

@router.post("/recover-password")
def recover_password(data: RecoverPasswordRequest, db: Session = Depends(get_db)):
    email = data.email

    user = db.query(UserDB).filter(UserDB.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token
    db.commit()

    # 🔥 DEEP LINK CORRECTO + EVITAR QUE RESEND LO ROMPA
    reset_link = f"manupilot://reset-password/{reset_token}"

    resend.Emails.send({
        "from": "ManuPilot Trail <onboarding@resend.dev>",
        "to": email,
        "subject": "Recupera tu contraseña",
        "disableLinkTracking": True,
        "html": f"""
            <h2>Recuperación de contraseña</h2>
            <p>Pulsa el siguiente enlace para restablecer tu contraseña:</p>
            <a href="{reset_link}">{reset_link}</a>
        """
    })

    return {"status": "ok", "message": "Email enviado para recuperar contraseña"}


# ---------------------------------------------------------
# RESET PASSWORD (POST)
# ---------------------------------------------------------
@router.post("/reset-password/{token}")
def reset_password(token: str, new_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.reset_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Token inválido")

    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    db.commit()

    return {"status": "ok", "message": "Contraseña actualizada"}


# ---------------------------------------------------------
# RESET PASSWORD (GET) → NO SE USA EN OPCIÓN 2
# ---------------------------------------------------------
@router.get("/reset-password/{token}")
def reset_password_page(token: str):
    return {
        "status": "ok",
        "message": "Token válido. Ahora envía la nueva contraseña por POST.",
        "token": token
    }
