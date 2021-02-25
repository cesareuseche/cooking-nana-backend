# importing the requests library 
import requests
import random 
import datetime

# Endpoint al que haremos POST  
API_ENDPOINT = "http://localhost:8080/recipes"
  
# Aquí iría la api_key en caso de haberla 
#API_KEY = "XXXXXXXXXXXXXXXXX"
  
# data to be sent to api 

    # Aquí va el código que genera los diccionarios
#source_ingredients = ["tomato", "rice", "beef", "chiken", "turkey", "pork", "partridge", "keema", "crab", "ham", "kidney meat", "mutton", "chops", "rocket leaves", "drumstick", "kaffir lime", "plantain", "cherry", "cherry tomatoes", "turnip", "gourd", "pimiento", "spinach", "onion", "mustard leaves", "radish", "amaranth", "flour", "oats", "jowar", "muesli", "tapioca", "semolina", "buckwheat", "green gram", "bengal gram", "kidney beans", "gruyere cheese", "gouda cheese", "milk", "feta cheese", "brie cheese", "cream cheese", "ricotta cheese", "parmesan cheese", "blue cheese", "cheedar cheese", "mascarpone cheese", "cream", "mozzarella cheese", "yogurt", "eggs", "salt", "sugar", "butter"]
name=[
    "Baked feta pasta",
    "Roast Sausages and Vegetables",
    "Classic Lasagne",
    "Homemade Pizza",
    "Homemade Pot Noodle",
    "Homemade Pasta Sauce",
    "Twice-Baked Potato",
    "Mexican Casserole",
    "One Pot Thai-Style Rice Noodles"
]

description = [
    "1 lb / 450 g italian durum wheat pasta, 1 block (7 oz / 200 g) greek feta cheese, 1/2 cup olive oil, 1/2 red chili pepper, 500 g cherry tomatoes, (4 garlic cloves if you wish), black pepper, salt, bunch of fresh basil leaves",
    "Pack of large Sausages, 500g Sweet Potatoes, chopped, One Broccoli head, 2 Red Onions, sliced, 3 Mixed Peppers, chopped, 1-2 Tbsp Olive Oil, Sprinkle of mixed herbs, Preheat oven to 200℃/ Fan 180℃/ Gas Mark 6.",
    "1 Onion, diced, 450g Beef Mince, 2 tins of Chopped Tomatoes, Sprinkle of mixed herbs, 4 Lasagne Sheets, Cheese, grated optional, Salad bag is optional, White Sauce: Knob of Butter, 100g Plain Flour, 250ml Milk (plus extra), Preheat oven to 180℃",
    "100g Self Raising Flour, 60ml Milk, 1 tbsp Olive Oil, 1 tin of Chopped Tomatoes, Sprinkle of Mixed Herbs, Any Toppings you like! (Pepperoni, ham, peppers, onions, mushrooms, chicken, pineapple etc), Cheese, grated, Preheat Oven to 200℃/ Fan 180℃/ Gas Mark 6.",
    "1 Nest of Noodles, 50g Frozen Peas and/or Veg, Half a Fresh Chilli, finely chopped or a pinch of chilli flakes, 2 Tbsp Chicken or Vegetable Stock, 3-4 Small Tomatoes",
    "1 tsp of Olive Oil, 1 tin of Chopped Tomatoes, 2 Garlic Cloves, finely chopped, 1 tbsp of Vegetable Stock, Sprinkle of Mixed Herbs, Cooked pasta, Cheese",
    "4 Large Baking Potatoes, 2 tbsp Olive Oil, 6 Spring Onions, sliced, 100g Bacon Lardons, 50g Unsalted butter, Salt and Pepper",
    "1 (16 ounce) can refried beans, ¾ onion, diced, 5 (10 inch) flour tortillas, 1 cup salsa, 2 cups shredded Cheddar or Colby Jack cheese",
    ""
]

ingredients = [
    ["pasta","cheese","olive oil","chili pepper","tomato","garlic","black pepper","salt","basil"],
    ["Sausage","Potato","Broccoli","onion","pepper","olive oil","Sprinkle of mixed herbs"],
    ["onion","beef","tomato","herbs","lasagne","cheese","salad","white sauce","butter","plain flour","milk"],
    ["Raising flour","milk","olive oil","tomato","herbs","cheese"],
    ["peas","chilli","tomato","chicken","mushrooms"],
    ["olive oil", "tomato","garlic","vegetable","herbs","pasta","cheese"],
    ["potatoes","olive oil","onions","bacon","butter"],
    ["beans","onion","flour tortillas","salsa","cheese"],
    ["cornstarch", "water","chicken broth","soy sauce","fish sauce","rice vinegar","chile-garlic sauce","vegetable oil","minced frechs ginger root","garlic","ground coriander","rice noodles","zucchini","red bell pepper","chicken breast", "peanuts","cilantro"]
]

instructions=[
    "Pour some olive on the bottom of the baking dish. Place the whole feta block on top. Chop the red chili pepper and add on top of feta cheese. Pour more olive oil on top. Place the cherry tomatoes on the sides and roll around in oil. Grind some pepper and season with pinch of salt. Bake in 400 F / 200 C for 15 minutes in the middle rack. Turn the heat to 440 F / 225 C, move the dish to the upper rack and use the grilling mode for another 10 minutes. Caution! This might cause the fire alarm to go off, mine does that every time. Cook the pasta al dente according to cooking instructions. If you used cherry tomatoes with stems, remove them. The stems are there merely for the instagrammable look, so plein cherry tomatoes will do fine. Break the feta a bit and mix with tomatoes. Mix the sauce with pasta and add plenty of basil leaves. Tip!  Garlic goes well with baked feta pasta. To add garlic cut four garlic cloves in half lengthwise, toss them in same time as the tomatoes and roll in olive oil.",
    "Preheat oven to 200℃/ Fan 180℃/ Gas Mark 6. Pour 1 tbsp of olive oil in a roasting or baking tray and place in oven for 5 minutes. Meanwhile, chop the sweet potatoes and mixed peppers. Place the sausages, sweet potatoes and peppers in the baking tray. Toss in the oil and roast for 15 minutes. Add the sliced red onions to the tray with a sprinkle of mixed herbs. Toss with the sausages and veg and roast for a further 10-15 minutes. Meanwhile, cook the broccoli in a pan of boiling water for 5 minutes. Drain and serve with the sausages and veg.",
    "Fry the onions in 1 tbsp of olive oil in a hot frying pan until soft. Add in mince and break up into small bits with a spatula or spoon that you’re using to stir. Once the mince is brown all over, add in the chopped tomatoes and mixed herbs and stir thoroughly. Boil and simmer for 15-20 minutes, stirring occasionally so the mince doesn’t stick to the bottom of the pan. Meanwhile, in a saucepan melt the knob of butter. Add in the flour and half the milk. Stir constantly on a medium heat to prevent lumps. The mixture will look yellow and thicken as you keep stirring so keep adding milk until the white sauce becomes white and to the thickness you desire. Turn the heat off. Place a lasagne sheet on the bottom of an ovenproof dish and then a large spoonful of the mince. Layer another lasagne sheet and add more mince. Repeat until all the mince is used up. Add a lasagne sheet on top and pour the white sauce on. Cook in the oven for 20 minutes. Serve with salad and cheese",
    "Prepare your toppings (e.g. Cut up the ham, grate the cheese). In a large bowl or mixing bowl, add the self raising flour, milk and oil. Mix with your hands to form the dough. Tip the dough onto a lightly floured surface and roll into a circle. Roll to the thickness of roughly two pound coins. Place on a baking tray. Spoon on your chopped tomatoes and spread near the edges of the dough. Sprinkle your mixed herbs on top. Add your toppings and cheese. Bake on top shelf for 20 minutes. Serve.",
    "Put all the ingredients in a bowl and pour in the boiling water. Let rest for 2-3 minutes, stirring occasionally. Serve. You can also put all the dry ingredients in a tall tupperware, take them to work or uni and add boiling water when it’s lunchtime!",
    "In a small saucepan, heat the Olive Oil. Add in the garlic and fry for 30 seconds. Pour in the chopped tomatoes and add the vegetable stock and mixed herbs. Stir until hot and add in cooked pasta. Stir until all the pasta is covered and if you want, sprinkle with cheese. Serve.",
    "Pierce potatoes all over with a fork, then rub half of the oil, salt and pepper onto the potatoes. Oven for 1 hour and 15 minutes. Fry the spring onion and bacon in the remaining olive oil. Once cooked, place on kitchen paper to slightly dry off. Half the potatoes lengthways (Caution! They will be hot) and scoop out the potato and place in a bowl. Mix the potato with the spring onions, bacon and butter. Scoop the mixture back into the potato skins. Top with cheese or butter and bake in the oven for a further 10-15 minutes. Serve.",
    "Preheat oven to 375 degrees F (190 degrees C). Spray a 9-inch pie pan with non-stick cooking spray. In a saucepan, cook refried beans and onions (to soften them) on medium-high heat for about 5 minutes. Place one tortilla in the bottom of the greased pan. Spread about 1/3 cup of the bean mixture over it. Layer a few tablespoons of salsa over this. Then, place another tortilla over the salsa, and add more of the bean mixture. Follow the beans with a big handful of cheese, spreading evenly. repeat layers, spreading the ingredients evenly over the tortillas. On the top layer, make sure to use lots of salsa and cheese! Bake until the cheese is melted, approximately 15 to 20 minutes.",
    ""
]

img_url = [
    "https://grilledcheesesocial.com/wp-content/uploads/2019/06/baked-feta-pasta-tomatoes-grilled-cheese-social-7-600x900.jpg",
    "https://simplebites.net/wp-content/uploads/2018/02/half-pan-cooked-1-e1517948247521.jpg",
    "https://www.perfectitaliano.com.au/content/dam/perfectitaliano-aus/recipe/0_desktop/Desktop-Classic-Beef-Lasagne.jpg.transform/image1220/image.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delish-homemade-pizza-horizontal-1542312378.png?crop=1.00xw:1.00xh;0,0&resize=980:*",
    "https://www.thelondoner.me/wp-content/uploads/2014/12/homemade-pot-noodle-20.jpg",
    "https://www.thespruceeats.com/thmb/4wYbxWuN6jICx0MxV1LpizKZsBk=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/classic-tomato-pasta-sauce-recipe-3992836-hero-01-8ad6cb1d12564635a23a0bfcdaee9980.jpg",
    "https://www.thecookierookie.com/wp-content/uploads/2018/05/twice-baked-potatoes-recipe-6-of-8.jpg",
    "https://cravinghomecooked.com/wp-content/uploads/2020/05/easy-mexican-casserole-1-750x938.jpg.webp",
    "https://www.halfbakedharvest.com/wp-content/uploads/2019/08/Better-Than-Takeout-Thai-Drunken-Noodles-1-768x1152.jpg"
]

for x in range(0, len(name)):
#for x in range (1,21): #el último número no se incluye en el For
    #sample_list = random.sample(source_ingredients, k=random.choice(range(1, len(source_ingredients))))
    #sample_list= [1]
    #print(sample_list)
    z = datetime.datetime.now()  
    datab = {"description":description[x],
            "name":name[x],
            "instructions":instructions[x],
            "tags":name[x],
            "img_url":img_url[x],
            "ingredients": ingredients[x],
            "date_published":str(z.year)+"-"+str(z.strftime("%m"))+"-"+str(z.strftime("%d"))+"T"+str(z.strftime("%H"))+":"+str(z.strftime("%M"))
            } 
    #print(datab)
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = datab) 
    print(f'receta {name[x]} agregada')
#extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url) 