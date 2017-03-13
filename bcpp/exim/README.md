# bcpp.exim

## Export Data

## Import Data

### Recipes

#### Using a recipe to import the default CSV:
    
    from bcpp.exim.import_data import site_recipes
    
    recipe = site_recipes.recipes.get('member.householdmember')
    
    # builds the dataframe and model instances without saving the model instance
    recipe.import_csv()
    
    # ... but save the model instance 
    recipe.import_csv(save=True)

#### Using the same recipe but get it to use non-default CSV

     ...
     recipe = site_recipes.recipes.get('member.householdmember')
     recipe.in_path = '/Users/erikvw/bcpp_201703/new/member/householdmember.consented.dups.csv'
     ...
     
#### Inspecting the dataframe

    recipe = site_recipes.recipes.get('member.householdmember')
    recipe.df
    
#### Modifying the DataFrame

The recipe can be configured to modify the dataframe to match to target DB table / django model. You can use the `pandas` dataframe methods to rename columns, remap a column, apply a function to a column, and drop columns. The `recipe` attributes are `df_rename_columns`, `df_add_columns`, `df_map_options`, `df_apply_functions`, and `df_drop_columns`. The methods are called in the same order:

    # rename
    df = df.rename(columns=[...])

    # add
    # for loop to add all columns in the list

    # map, e.g.
    df[colname] = df['colname'].map(options.get)
    
    # apply, e.g.
    df = df.apply(lambda row: your_func(row), axis=1)
    
    # drop, e.g.
    df = df.drop(colname, axis=1)


