from operator import and_
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import Schema
from Database import model
from datetime import datetime

def All_Property(db:Session):
    property = db.query(model.Property).filter(and_(model.Property.status == True, model.Property.sell == True)).all()
    result = [Schema.PropertyToBuy(name = p.name, number = p.number, owner=p.owner, description=p.desc, location=p.location, pincode=p.pincode, price=p.sell_price) for p in property]
    return result

def Extract_PropertyData(property:str, username:str, db:Session):
    propertydata = db.query(model.Property).filter(and_(model.Property.status == True, model.Property.number == property, model.Property.sell == True)).first()
    result = Schema.BuyPropertyForm(number=property, owner = propertydata.owner, customer=username, price=propertydata.sell_price, taxes=(0.18*propertydata.sell_price), total_price=(propertydata.sell_price+(0.18*propertydata.sell_price)))
    return result

def Submit_Purchase(data:Schema.SubmitBuyProperty, username:str, db:Session):
    if username == data.customer:
        try:
            new_record = model.BuyRecord(property=data.number, owner=data.owner, customer=data.customer, price = data.price, tax = data.taxes, total=data.total_price, token=data.token, purchasedate=datetime.today().strftime('%Y-%m-%d'), verification = 'False')
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return new_record
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Unable to register due to issue: {e}')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please register from same id from which you selected the property')