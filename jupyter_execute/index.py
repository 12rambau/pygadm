#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygadm

gdf = pygadm.get_items(name="Singapore", content_level=1)
gdf.plot(cmap="viridis")
