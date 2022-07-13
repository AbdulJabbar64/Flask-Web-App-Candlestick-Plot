from flask import Flask, render_template

app = Flask(__name__)

@app.route("/plot/")
def plot():
    from bokeh.embed import components
    from bokeh.resources import CDN
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, output_file, show
    start = datetime.datetime(2015,11,1)
    end = datetime.datetime(2016,3,10)
    df = data.DataReader("GOOG",data_source="yahoo",start=start, end=end)
    df.head()
    def inc_dec(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["status"] = [inc_dec(c, o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)
    f = figure(x_axis_type="datetime", height=300, width=1000)
    f.title = "Candlestick Chart"
    f.sizing_mode="scale_width"
    f.grid.grid_line_alpha=0.3
    hour_12= 12*60*60*1000
    f.segment(df.index, df.High,df.index,df.Low, color="black")
    f.rect(df.index[df.status=="Increase"], df.Middle[df.status=="Increase"] ,
        hour_12, df.Height[df.status=="Increase"], fill_color="green", line_color="black")

    f.rect(df.index[df.status=="Decrease"], df.Middle[df.status=="Decrease"] ,
        hour_12, df.Height[df.status=="Decrease"], fill_color="red", line_color="black")

    # output_file("Candle.html")
    # show(f)
    script1, div1 = components(f)
    cdn_js = CDN.js_files[0]

    return render_template("plot.html", script1=script1, div1=div1, cdn_js= cdn_js)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/")
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)