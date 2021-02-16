from marshmallow import Serializer

###### USER SERIALIZER #####
class RecipeSerializer(Serializer):
    class Meta:
        # Fields to expose
        fields = ('ingredients')
        # you can add any other member of class user in fields

#Return the user data in json format
def get_user_serialized(recipe):
    return UserSerializer(user).data