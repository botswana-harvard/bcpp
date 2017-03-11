# bcpp.exim

## Export Data

## Import Data

### Recipes

Using a recipe to import the default CSV:
    
    from bcpp.exim.import_data import site_recipes
    
    recipe = site_recipes.recipes.get('member.householdmember')
    
    # builds the dataframe and model instances without saving the model instance
    recipe.import_csv()
    
    # ... but save the model instance 
    recipe.import_csv(save=True)

Using the same recipe but get it to use non-default CSV

     ...
     recipe = site_recipes.recipes.get('member.householdmember')
     recipe.in_path = '/Users/erikvw/bcpp_201703/new/member/householdmember.consented.dups.csv'
     ...
     
Inspecting the dataframe

    recipe = site_recipes.recipes.get('member.householdmember')
    recipe.df