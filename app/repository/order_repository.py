from sqlalchemy.orm import Session, joinedload
from starlette import status
import database.models as models, database.schema as schema


def create_order(request:schema.Order, response, db:Session, current_user:schema.User ): 
    # order = db.query(models.Order).filter(models.Order.name == request.name).first()
    
    # if order:
    #     response.status_code = status.HTTP_409_CONFLICT
    #     return {
    #         'message': "order already exist",
    #         'status_code': 409,
    #         'error': 'CONFLICT'
    #     }
    
    new_order = models.Order(
        owner_id = current_user.id,
        # name = request.name,
        quantity = request.quantity, 
        order_size = request.order_size
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': new_order.id,
            'datails': new_order.quantity
        }
    }


def all_orders(db:Session, current_user:schema.User):
    
    all_orders = db.query(
            models.Order
        ).filter(
            models.Order.user.has(id=current_user.id)
        ).order_by(
            models.Order.id.desc()
        ).all()
    
    return all_orders


def get_order(order_id:int, response, db:Session, current_user:schema.User):
    
    order = db.query(
            models.Order
        ).filter(
            models.Order.id == order_id,
            models.Order.user.has(id=current_user.id)
        ).first()
        
    if not order:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    return {
        'data': order
    }
  
    
def update_order(order_id:int, request:schema.Order, response, db:Session, current_user:schema.User):
    
    ordered = db.query(
            models.Order
        ).filter(
            models.Order.id == order_id,
            models.Order.user.has(id=current_user.id)
        ).first()
        
    if not ordered:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
        
    # ordered.name = request.name
    ordered.quantity = request.quantity
    ordered.order_size = request.order_size
    
    db.add(ordered)
    db.commit()
    db.refresh(ordered)
    
    return {
        'message': "successful",
        'status_code': 201,
        'status': 'Success',
        'data': ordered
    }


def delete_order(order_id:int, response, db:Session, current_user:schema.User):
    
    ordered = db.query(
            models.Order
        ).filter(
            models.Order.id == order_id,
            models.Order.user.has(id=current_user.id)
        ).delete(synchronize_session=False)
    
    db.commit()
    
    if not ordered:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND',
        }
    return {
        'message': "Deleted successfully",
        'status_code': 200,
        'status': 'Success',
        'data': ordered
    }