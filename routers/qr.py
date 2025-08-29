from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import base64
import io
from PIL import Image
import numpy as np

from models import Usuario
from schemas import QRValidationRequest, QRValidationResponse
from database import SessionLocal
from routers.auth import get_current_user

router = APIRouter(prefix="/qr", tags=["Validación QR"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_recycling_image(image_data: str) -> bool:
    """
    Función para validar si la imagen muestra reciclaje válido.
    En un caso real, aquí usarías un modelo de IA entrenado.
    Por ahora, simulamos la validación.
    """
    try:
        # Decodificar imagen base64
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a array numpy para análisis
        img_array = np.array(image)
        
        # Simulación de validación de IA
        # En un caso real, aquí pasarías la imagen a tu modelo de IA
        
        # Por ahora, simulamos que el 80% de las imágenes son válidas
        # Esto es solo para demostración
        import random
        is_valid = random.random() < 0.8
        
        return is_valid
        
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return False

@router.post("/validate", response_model=QRValidationResponse)
def validate_qr(
    qr_data: QRValidationRequest, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Valida el reciclaje basado en el código QR y la imagen.
    """
    try:
        # Verificar que el usuario existe
        user = db.query(Usuario).filter(Usuario.id == qr_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Validar la imagen usando IA (simulado)
        is_valid = validate_recycling_image(qr_data.image_data)
        
        # Determinar puntos a otorgar
        cleanpoints_earned = 50 if is_valid else 0
        
        # Mensaje de respuesta
        if is_valid:
            message = "¡Reciclaje validado exitosamente! Has ganado 50 CleanPoints por contribuir al medio ambiente."
            
            # Actualizar CleanPoints del usuario
            user.cleanpoints += cleanpoints_earned
            # Incrementar conteo de items reciclados (persistente)
            if getattr(user, 'total_recycled_items', None) is None:
                user.total_recycled_items = 0
            user.total_recycled_items += 1
            db.commit()
        else:
            message = "La imagen no muestra un reciclaje válido. Por favor, asegúrate de que la imagen muestre claramente el material a reciclar."
        
        # Crear respuesta
        response = QRValidationResponse(
            success=True,
            valid=is_valid,
            cleanpoints_earned=cleanpoints_earned,
            message=message,
            timestamp=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        print(f"Error en validación QR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor durante la validación"
        )

@router.post("/test")
def test_qr_endpoint():
    """
    Endpoint de prueba para verificar que el router funciona.
    """
    return {
        "message": "Endpoint QR funcionando correctamente",
        "timestamp": datetime.utcnow(),
        "status": "success"
    }
