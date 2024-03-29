# -*- coding: utf-8 -*-

# MAIN FILE:  "spotify_user_auth"

#%%  Authentication
"""
PROBLEM WITH TOKEN AFTER PASSWORD RESET: 
    In my case the token had not expired, but was changed (probably because of 
    a forced password change by spotify), which led to "wrongful calls".
    Spotipy was not able to resolve this issue automatically. 
  SOLUTION:
      Manually deleting the ".cache" file solved this issue by refreshing the
      token 
    
# Spotipy is supposed to do the following:
# 1. Check ".cache" file (or ".cache-<username>")
# 2. If its expired -> refresh it
# 3. If not in ".cache" open browser and store it in ".cache"
# https://stackoverflow.com/questions/48883731/refresh-token-spotipy

### My own thoughts
I suppose this (redirect_uri) is where the data is being sent to, where
we access the data?  Therefore it is also a "local" target.
We might, I guess, put up a server target (https://cross_sync.com:8080/callback)
to handle responses to certain server? apps.
redirect_uri  = sp_api_url # redirect to spotify API call
Does not work with this code, hence the above
"""

#%%  getting data
###########################################################################
##################          My top tracks (mtt)        ####################
#   - my most listened to tracks (so far this year) 
if os.path.exists("data/my_top_50.csv"): 
    mtt = pd.read_csv("data/my_top_50.csv")
else: 
    # get my top 50 songs (so far: 2023.03.11)
    mtt = lib.top_tracks_df(sp) 
    mtt = mtt.set_index(mtt.index+1)      # set new index
    mtt.to_csv("data/my_top_50.csv", index = False) # save it 

########        My top 50 track (recent) features        ##########
#     - top 50 tracks (so far this year)
if os.path.exists("data/my_top_50_features.csv"): 
    msgf = pd.read_csv("data/my_top_50_features.csv")
else:
    # a move basic feature pack (simpler to graph)    
    # my song general features
    msgf = sp.audio_features(mtt["uri"])        # get features
    msgf = pd.DataFrame(msgf)                   # dataframe features
    msgf = msgf.drop(["id","track_href", "analysis_url","type"], axis = 1) # drop useless columns 
    msgf = msgf.set_index(msgf.index + 1)
    msgf.to_csv("data/my_top_50_features.csv", index = False) # save


###############################################################################
#################           My top 50 all time              ###################
if os.path.exist("data/my_top_50_all_time.csv"):
    mttat = pd.read_csv("data/my_top_50_all_time.csv")
else:
    mttat = lib.top_tracks_df(sp, limit = 50, time_range = "long_term") # get top tracks all time
    mttat = mttat.set_index(mttat.index + 1) # fix index
    mttat.to_csv("data/my_top_50_all_time.csv")
    
###########            My top 50 all time features          ##################
if os.path.exist("data/my_top_50_all_time_features.csv"):
    mttatf = pd.read_csv("data/my_top_50_all_time_features.csv")
else:
    mttatf = sp.audio_features(mttat["uri"])
    mttatf = pd.DataFrame(mttatf)
    mttatf = mttatf.drop(["id","track_href", "analysis_url","type"], axis = 1) # drop useless columns
    mttatf = mttatf.set_index(mttatf.index + 1)
    mttatf.to_csv("data/my_top_50_all_time_features.csv")
    
############################################################################### 
#########          My top track (recent) analysis (mtta)       ################
#   - My top 50 songs audio analysis
# A more specific analysis 
if os.path.exists("data/my_top_50_specifics.csv"):
    mtta = pd.read_csv("data/my_top_50_specifics.csv")
else:
    mtta = track_analysis_to_df(mtt["uri"]) # get features
    mtta["culminative_time"] = pd.NA # new var
    for value in mtta.index:
        if mtta["track index"][value] == 0: # if we start a new track we start from this "time" value
            mtta["culminative_time"][value] = mtta["time"][value]
                    
            mtta.loc[value,"culminative_time"]
        elif mtta["track index"][value] > 0: # if we are on the same track, we continue from last value 
            mtta["culminative_time"][value] = mtta["culminative_time"][value-1] + mtta["time"][value]
    mtta.to_csv("data/my_top_50_specifics.csv", index = False)

###############################################################################
###########              Norway top 50 (nt50) songs              ##############
# as of 16.03.2023 
if os.path.exists("daata/norway_top_50-16.03.2023.csv"):
    nt50 = pd.read_csv("data/norway_top_50-16.03.2023.csv")
else: 
    # https://open.spotify.com/playlist/37i9dQZEVXbJvfa0Yxg7E7
    nt50 = lib.playlist_to_df(sp, "37i9dQZEVXbJvfa0Yxg7E7") # Get playlist to df
    nt50 = nt50.set_index(nt50.index + 1)      # set new index
    nt50.to_csv("data/norway_top_50-16.03.2023.csv")
    

# %% Subset
"""
# get out my favorite song features
# mtsf = my_top_song_features
mtsf = mtta[mtta["song index"] == 0] # subset of my top song.


##### MAYBE NOT, BELOW
# %%  Pivot dataframe for seaborn graph:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html
mtsf_long = pd.wide_to_long(mtsf,
                            #we want togather  timbre and pitch to one variable
                            stubnames = ["timbre", "pitch"],  
                            sep = "-", # get all timbre based on a "-" split ("timbre-"1 /// timbre-"2)
                            i = "track index",  # based on track index
                            j = "value_index")  # give it a new variable "track_index"

mtsf_long = mtsf_long.reset_index() # add our indexs to the dataframe 

# double seaborn (based on columns?):  https://seaborn.pydata.org/tutorial/relational.html
    # require pivot? 

# %%   Seaborn data selection 
# https://stackoverflow.com/a/65012723
vals = [2,3,5]
sb.relplot(mtsf_long.loc[mtsf_long.value_index.isin(vals)],
           x = "culminative_time", 
           y = "timbre",
           kind = "line",
           col = "value_index",
           hue = "value_index", ) 
#%%
sb.lineplot(mtsf_long.loc[mtsf_long.value_index.isin(vals)],
           x = "culminative_time", 
           y = "timbre", "loudness_max",
           hue = "value_index",)

#<<<<<<zzzz
f2, ax1 = sb

test = sb.relplot(my_top_song_features, x = "culminative_time", y = "timbre-1", kind = "line")

test.set_titles("test")

test.axes_dict.items()

ax = sb.relplot(my_top_song_features, x = "culminative_time", y = "pitch-7", kind = "line")

sb.relplot(my_top_song_features, x = "culminative_time", y = "timbre-2", kind="line")

sb.relplot(my_top_song_features, x = "culminative_time", y = "timbre-3", kind="line")
### ---
"""


"""
# double plotting in matplotlib: https://matplotlib.org/stable/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py
# https://stackoverflow.com/a/8228808
 - plt.cla() clears an axis, i.e. the currently active axis in the current figure. It leaves the other axes untouched.
 - plt.clf() clears the entire current figure with all its axes, but leaves the window opened, such that it may be reused for other plots.
 - plt.close() closes a window, which will be the current window, if not specified otherwise.

# Thus we can make ONE FIGURE, ADD TO IT (ax) and clear it! 

Why am i missing help information on "ax" variable:
    lookup: https://matplotlib.org/stable/api/axes_api.html#basic
# to interpret features of track analysis: 
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features

# compare my music features to top 50 of norway ?
# https://open.spotify.com/playlist/37i9dQZEVXbJvfa0Yxg7E7?si=94da68a1315a418f
"""
# %% VISUALIZE #### 
plt.show()

#%% HIST 

fig3, ax3 = plt.subplots()
plt.cla()
ax3.hist(dp["danceability"], alpha = 0.4, color = "#4dac26")
ax3.hist(dp2["danceability"], alpha = 0.4, color = "#d0278b")
    


ax3.bar( height = dp["danceability"], alpha = 0.7, color = "blue")
plt.hist(dp["energy"],)
plt.hist(dp2["energy"])
#%% VERTICAL PLOT
fig2, (ax1, ax2) = plt.subplots(1,2) # to vertical


ax1.plot(dp.index, dp["danceability"])
# Using "dp" (data_plotting) to be able to quickly change data input in graph 
 
plt.cla()
# set background colour 
ax.set_facecolor("#e0e0e0")
ax.grid()
ax.set_xticks(np.arange(0.0,1.1,0.1))
ax.set_xtitle()
ax.set_yticks(np.arange(0.0,1.1,0.1))





ax.fill_between(dp.index, dp["danceability"], dp["speechiness"])
ax.fill_between(dp.index, dp["speechiness"])
ax.fill_between(dp.index, dp["danceability"],.9)

#ax.plot(msgf.index, msgf["tempo"], c ="purple", linewidth = 3)

ax.plot(dp.index, dp["loudness"], linewidth = 3)
ax.plot(msgf_10.index, np.log10(abs(msgf_10["loudness"])), linewidth = 3)
ax.set_xticks(np.arange(1,51,1))


ax.plot(msgf_10.index, msgf_10["danceability"])


plt.cla()




# %%  IF I WANT, I can do more "fine grane analysis of a specific track:
special = track_analysis_to_df(["5QdATOQJp1kififgPZYQ2Q"])

sp.audio_analysis("5QdATOQJp1kififgPZYQ2Q")
# ANALYSIS OF: 5QdATOQJp1kififgPZYQ2Q

# add loudness - do something fancy here
ax.plot(mtsf["culminative_time"], mtsf["loudness_max"])


ax.set_yticks(np.arange(-60,0,5))
ax.set_title("Loudness over time units")
ax.set_ylabel("Loudness")
ax.set_title("")
ax
plt.cla()

fig

ax.plot(mtsf["culminative_time"], mtsf["timbre-2"]) # add timbre 2
ax.plot(mtsf["culminative_time"], mtsf["timbre-3"]) # add timbre 3


# pitch to plot 
ax.plot(mtsf["culminative_time"], mtsf["pitch-1"]) # add

# log transform to fit pitch in plot: 
# https://www.geeksforgeeks.org/log-and-natural-logarithmic-value-of-a-column-in-pandas-python/
np.log(mtsf.loc[:,"timbre-1":"timbre-12"])
np.log(mtsf.loc[:,"timbre-2"])


# grand mean over pitch
# https://statisticsglobe.com/calculate-mean-python
ax.plot(mtsf["culminative_time"], mtsf.loc[:,"timbre-1":"timbre-12"].mean(axis=1))




# SET OTHER INFORMATION TO "AX"
# ax.set_yticks(np.arange(-200,100,20))



#%%  Corr matrix
labels = df.applymap(lambda v: v if v < 0.05 else ' ')

# We can apply over multiple 
pvals = df.corr(method=lambda x, y: s.pearsonr(x, y)[1])# < 0.05

# Create significant correlational markers 
p_values = np.tril(df.corr(method='pearson'), k=-1)
t1 = np.abs(p_values) < 0.05 # condition one 
t2 = np.abs(p_values) == 1   # condition two
mask = np.logical_or(t1,t2)  # combine 
