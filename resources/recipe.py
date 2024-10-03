from models import RecipeModel, db
from flask_restful import Resource,fields, marshal,reqparse, marshal_with
from flask_jwt_extended import current_user, jwt_required

recipe_fields={
    "id": fields.Integer,
    "title": fields.String,
    "ingredients": fields.String,
    "instructions": fields.String,
    "cooking_time": fields.String
}


class Recipe(Resource):
    recipe_parser = reqparse.RequestParser()
    recipe_parser.add_argument("title",required=True,type=str,help="please input the title")
    recipe_parser.add_argument("ingredients",required=True,type=str,help="please input the ingredients")
    recipe_parser.add_argument("instructions",required=True,type=str,help="please input the instructions")
    recipe_parser.add_argument("cooking_time",required=True,type=str,help="please input the cook time")
    
    @marshal_with(recipe_fields)    
    def get(self,id=None):
        if id:
            recipe = RecipeModel.query.filter_by(id=id).first()
            if recipe == None:
               return {"message":"Recipe not found"}, 404
            return marshal(recipe, recipe_fields)
        else:
            recipes = RecipeModel.query.all()
            return  marshal(recipes, recipe_fields)

    @jwt_required()  
    def post(self):
        
        
        data = Recipe.recipe_parser.parse_args()

        recipe = RecipeModel(**data)


        try:
            db.session.add(recipe)
            db.session.commit()

            return {"message":"Recipe created successfully"}
        except:
            return {"message" : "unable to create recipe"}
        

    def patch(self,id):
        data = Recipe.recipe_parser.parse_args()
        recipe = RecipeModel.query.get(id)

        if recipe:
            for key,value in data.items():
                setattr(recipe,key,value)
            try:
                db.session.commit()

                return {"message":"recipe updated successfully"}
            except:
                return {"message":"recipe unable to be updated"}
            
        else:
            return {"message":"recipe not found"}
        

    @jwt_required() 
    def delete(self,id):
        
        recipe = RecipeModel.query.get(id)
        if recipe:
            try:
                db.session.delete(recipe)
                db.session.commit()

                return {"message":"recipe deleted"}
            except:
                return {"message":"recipe unable to be deleted"}
        else:
            return {"message":"recipe not found"}


    
    
