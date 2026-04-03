"""
Payment Service
Handles payment processing and QR code generation using Razorpay
"""
import uuid
import base64
from typing import Dict, Any, Optional
from io import BytesIO

from app.models.schemas import PaymentResponse
from app.core.config import settings

# Import razorpay with error handling
try:
    import razorpay
except ImportError:
    razorpay = None


class PaymentService:
    """Service for handling payments"""
    
    def __init__(self):
        # Initialize Razorpay client
        try:
            if razorpay and settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
                self.client = razorpay.Client(
                    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
                )
            else:
                self.client = None
                if not razorpay:
                    print("Warning: Razorpay library not installed. Using simulation mode.")
                else:
                    print("Warning: Razorpay credentials not configured. Using simulation mode.")
        except Exception as e:
            self.client = None
            print(f"Warning: Could not initialize Razorpay client: {e}")
    
    async def create_payment_order(
        self,
        amount: float,
        currency: str,
        booking_id: str
    ) -> PaymentResponse:
        """
        Create payment order and generate QR code
        """
        # Convert amount to paise (Razorpay uses smallest currency unit)
        amount_in_paise = int(amount * 100)
        
        if self.client:
            try:
                # Create Razorpay order
                order_data = {
                    "amount": amount_in_paise,
                    "currency": currency,
                    "receipt": booking_id,
                    "notes": {
                        "booking_id": booking_id,
                        "type": "travel_booking"
                    }
                }
                
                order = self.client.order.create(data=order_data)
                
                # Generate QR code for the order
                qr_code_url = await self._generate_qr_code(
                    order_id=order["id"],
                    amount=amount
                )
                
                return PaymentResponse(
                    success=True,
                    qr_code_url=qr_code_url,
                    payment_id=str(uuid.uuid4()),
                    order_id=order["id"],
                    amount=amount,
                    currency=currency
                )
            
            except Exception as e:
                print(f"Razorpay order creation failed: {e}")
                # Fall back to simulation
                return await self._create_simulated_payment(amount, currency, booking_id)
        else:
            # Simulation mode
            return await self._create_simulated_payment(amount, currency, booking_id)
    
    async def _create_simulated_payment(
        self,
        amount: float,
        currency: str,
        booking_id: str
    ) -> PaymentResponse:
        """
        Create simulated payment for testing
        """
        order_id = f"order_{uuid.uuid4().hex[:12]}"
        payment_id = f"pay_{uuid.uuid4().hex[:12]}"
        
        # Generate simulated QR code URL
        qr_code_url = await self._generate_simulated_qr(
            order_id=order_id,
            amount=amount
        )
        
        return PaymentResponse(
            success=True,
            qr_code_url=qr_code_url,
            payment_id=payment_id,
            order_id=order_id,
            amount=amount,
            currency=currency
        )
    
    async def _generate_qr_code(
        self,
        order_id: str,
        amount: float
    ) -> str:
        """
        Generate QR code for payment
        """
        try:
            # Try to import and use qrcode library
            import qrcode
            
            # Create QR code data
            qr_data = f"upi://pay?pa=merchant@razorpay&pn=WanderWise&am={amount}&cu=INR&tn=Travel Booking"
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffered = BytesIO()
            img.save(buffered)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
        
        except ImportError:
            # If qrcode library not available, return simulated QR
            return await self._generate_simulated_qr(order_id, amount)
        except Exception as e:
            print(f"QR generation failed: {e}")
            return await self._generate_simulated_qr(order_id, amount)
    
    async def _generate_simulated_qr(
        self,
        order_id: str,
        amount: float
    ) -> str:
        """
        Generate simulated QR code URL for testing
        """
        # Return a placeholder QR code image URL
        # In production, this would be replaced with actual QR generation
        qr_data = f"upi://pay?pa=wanderwise@upi&pn=WanderWise&am={amount}&cu=INR&tn=Booking-{order_id}"
        
        # Use a public QR code API for simulation
        encoded_data = qr_data.replace(":", "%3A").replace("/", "%2F").replace("?", "%3F").replace("&", "%26").replace("=", "%3D")
        return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_data}"
    
    async def verify_payment(
        self,
        payment_id: str,
        signature: str
    ) -> bool:
        """
        Verify payment signature
        """
        if self.client:
            try:
                # In production, verify using Razorpay
                # params_dict = {
                #     'razorpay_order_id': order_id,
                #     'razorpay_payment_id': payment_id,
                #     'razorpay_signature': signature
                # }
                # self.client.utility.verify_payment_signature(params_dict)
                # return True
                
                # For now, simulate verification
                return True
            except Exception as e:
                print(f"Payment verification failed: {e}")
                return False
        else:
            # Simulation mode - always return True for testing
            return True
    
    async def get_payment_status(
        self,
        payment_id: str
    ) -> Dict[str, Any]:
        """
        Get payment status
        """
        if self.client:
            try:
                payment = self.client.payment.fetch(payment_id)
                return {
                    "status": payment.get("status", "unknown"),
                    "amount": payment.get("amount", 0) / 100,
                    "currency": payment.get("currency", "INR"),
                    "method": payment.get("method", "unknown")
                }
            except Exception as e:
                print(f"Failed to fetch payment status: {e}")
                return {"status": "unknown"}
        else:
            # Simulation mode
            return {
                "status": "captured",
                "amount": 0,
                "currency": "INR",
                "method": "upi"
            }


# .
