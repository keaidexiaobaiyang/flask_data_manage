from app import create_app
from flask_sqlalchemy import SQLAlchemy
app = create_app()

#app.run(host='0.0.0.0',port=10520,debug=True)
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)