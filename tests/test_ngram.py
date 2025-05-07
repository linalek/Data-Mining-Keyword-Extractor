from src.ngram import create_n_grams

######################################### Test1 ########################################
print("\n\n\n\n")
stop_words:list = [",",".","!"]
tokens:list = ["Ola",",","seja","bem-vindo","ao","mundo",".","Adeus", "não" ,"volte", "mais" ,"!"]

returned_dict = create_n_grams(tokens,stop_words)
print(returned_dict)
print()
print( len(returned_dict)>len(tokens))

######################################### Test2 ########################################
