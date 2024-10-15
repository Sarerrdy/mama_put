import logging
import json
import time

from flask import request
from flask_restful import Resource, abort, current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import jwt

from database import db
from models.order import Order
from models.order_details import Order_Detail
from schemas.order_schema import OrderSchema
from schemas.order_details_schema import OrderDetailsSchema
# from schemas.menu_order_schema import MenuOrderSchema

ORDERS_ENDPOINT = "/api/orders"
logger = logging.getLogger(__name__)


def verify_auth_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])
    except:
        return
    return data


def generate_auth_token(self, expires_in=60):
    return jwt.encode(
        {'sub': "12345", 'exp': time.time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')


class OrdersResource(Resource):
    def get(self, id=None):
        """
        OrdersResource GET method. Retrieves all orders found in the mamaput
        database, unless the id path parameter is provided. If this id
        is provided then the order with the associated id is retrieved.

        :param id: Order ID to retrieve, this path parameter is optional
        :return: Order, 200 HTTP status code
        """
        if request.endpoint == "checkerToken":
            return self._get_checker(), 200
        # if request.endpoint == "verifycheckerToken":
        #     return self._verify_checker(), 200

        if not id:
            status = request.args.get("status")
            checkerToken = request.args.get("checkerToken")
            logger.info(
                f"Retrieving all orders, optionally filtered by "
                f"status={status}"
            )
            if checkerToken:
                return self._verify_checker(checkerToken), 200
            return self._get_all_orders(status), 200

        logger.info(f"Retrieving orders by id {id}")

        try:
            return self._get_order_by_id(id), 200
        except NoResultFound:
            abort(404, message="order not found")

    def _get_order_by_id(self, order_id):
        """retrieve order by order id"""
        order = Order.query.filter_by(order_id=order_id).first()
        order_json = OrderSchema().dump(order)

        if not order_json:
            raise NoResultFound()

        logger.info(f"Order retrieved from database {order_json}")
        return order_json

    def _get_all_orders(self, status):
        """retrieve all order"""
        if status:
            orders = Order.query.filter_by(status=status).all()
        else:
            orders = Order.query.all()

        orders_json = [
            OrderSchema().dump(order) for order in orders]

        logger.info("Orders successfully retrieved.")
        return orders_json

    def _get_checker(self):
        """generate unique order identifier"""
        token = generate_auth_token(60)
        return token

    def _verify_checker(self, token):
        """check validity of Token"""
        token = verify_auth_token(token)
        logger.info(f"Token: {token}")
        if token:
            logger.info("Token correct")
            return True
        logger.info("Token failed")
        return False

    def post(self):
        """
        OrdersResource POST method. Adds a new order item to the database.

        :return: order.order_id, 201 HTTP status code.
        """
        req_data = request.get_json()        
        neworder = req_data["orders"]["order"]        
        orderDetails = req_data["orders"]["order_details"]
        newAddress = req_data["orders"]["newAddressArgs"] 
        payment = req_data["orders"]["payment"] 
        shipping = req_data["orders"]["shipping"]
       

        order = OrderSchema().load(neworder)
        order.date_ordered = datetime.now()        

        orderDetailsSchema = OrderDetailsSchema(many=True)
        orderDts = orderDetailsSchema.load(orderDetails)

        try:

            db.session.add(order)
            # update order details
            for orderDetail in orderDts:                
                orderDetail.order = order
                orderDetail.order_id = order.order_id

            db.session.add_all(orderDts)
            db.session.commit()

        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this order is already in the database. "
                f"Error: {e}"
            )
            abort(500, message="Unexpected Error!")
        else:           
            return order.order_id, 201
