from flask import Flask, render_template, request, jsonify, make_response
from googlesearch import search
from extract_image import get_images
from extract_image import get_image
from extract_image import get_images_concurrently
import time
import concurrent.futures


query=None
db=list()
database=list()
total_results=25
posts=total_results
quantity=3

def append_image(row):
    row.append(get_image(row[1]))
    return row


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/', methods=['POST'])
def getvalue():
    global query,db,database,total_results,posts,quantity
    query=request.form['query']
    
    db=search(query, number_of_query=25)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        database=list(executor.map(append_image, db))

    quantity=3
    
    total_results=len(db)
    posts=total_results

    return render_template('results.html', query=query)

@app.route("/load")
def load():
    """ Route to return the posts """

    #time.sleep(0.2)  # Used to simulate delay
    
    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            #print("Returning posts 0 to "+str(quantity)+" "+str(total_results))
            # Slice 0 -> quantity from the db

            # print(db[0])
            # for i in range(quantity):
            #     print('extracting image for '+str(i))
            #     db[i].append(get_image(db[i][1]))

                
            
            res = make_response(jsonify(database[0: min(quantity, total_results)]), total_results)

        elif counter == posts:
            print("No more results")
            res = make_response(jsonify({}), total_results)

        else:
            #print("Returning posts "+str(counter)+" to "+str(counter + quantity))
            # Slice counter -> quantity from the db

            # for i in range(counter,counter+quantity):
            #     print('extracting image for '+str(i))
            #     db[i].append(get_image(db[i][1]))

            res = make_response(jsonify(database[counter: min(counter + quantity,total_results)]), total_results)

    return res

@app.route('/getimage', methods=['POST'])
def getimg():
    link=request.get_data().decode("utf-8")
    print(link,type(link))
    # if request.args:
    #     link=str(request.args.get("link"))
    image_url=get_image(link)
    #print(image_url)
    #res = make_response(jsonify(image_url))
    #print(res)
    #return res
    return make_response(jsonify(image_url))

@app.route('/getimg')
def get_img():
    
    if request.args:
        link=str(request.args.get("link"))
        image_url=get_image(link)
    res = make_response(jsonify(image_url))
    return res


if __name__=='__main__':
    app.run(debug=True)