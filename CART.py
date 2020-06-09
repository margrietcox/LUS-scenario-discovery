x = experiments
y = clustering

cart_alg = cart.CART(x, y, mass_min = 0.5, mode = RuleInductionType.CLASSIFICATION)


cart_alg.build_tree()


cart_alg.stats_to_dataframe()
cart_alg.boxes_to_dataframe()
    
cart_alg.show_boxes(together=False)
plt.show()

tree = cart_alg.show_tree()
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.show()
   
    
    
    
 



            