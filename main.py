import requests
from flask import Flask, render_template, request
from pprint import pprint 
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

app = Flask(__name__)

#
#  set some variables
#
local_path=os.path.expanduser("~/Documents")
local_file_name ="fatheadHopJuju.png"
container_name ='quickstartblobs'
local_file_name ="fatheadHopJuju.png"
local_path=os.path.expanduser("~/Documents/UPLOAD")
#  set the subscription key from Azure Cognitive Services Resource Group
#
#
#  set the region to use and the url/resource_path for the API nethond
#
region = 'westcentralus' #Here you enter the region of your subscription
url = 'https://{}.api.cognitive.microsoft.com/vision/v1.0/analyze'.format(region)
key = "nononeedhelpfwithdf"
pic = "static/img/person.jpg"

storage_account = 'inststorageaccount'
account_key = 'nonaneedshelppickinganimals'

@app.route('/')
def index():
  return render_template("index.html") 

@app.route("/about")
def about():
  req = requests.get('https://github.com/timeline.json')
  treq = req.url 
  resp = req.json()
  return render_template("about.html", url=treq, result=resp)

@app.route("/vision")
def vision():

  maxNumRetries = 1

  pathToFileInDisk = pic
  with open( pathToFileInDisk, 'rb' ) as f:
    data = f.read()

# Computer Vision parameters
  params = { 'visualFeatures' : 'categories,tags,description,faces'}

# Computer Vision header fields
  headers = dict()
  headers['Ocp-Apim-Subscription-Key'] = key
  headers['Content-Type'] = 'application/octet-stream'

  json = None
  response = requests.request( 'post', url, json = json, data = data, headers = headers, params = params )

  vreq = response.url 
  vresp = response.text

  return render_template("vision.html", url=vreq, result=vresp, pic=pic)
  
@app.route('/selcvfile')
def selcvfile():
  return render_template("selcvfile.html") 
  
@app.route("/upload", methods = {'GET', 'POST'})
def upload():
  
  if request.method == 'POST':
     
     req_file = request.files['file']
     print("in POST if, filename is " + req_file.filename)
     local_file_name = req_file.filename
     full_path_to_file = os.path.join(local_path, local_file_name)
     req_file.save(os.path.join(local_path, local_file_name))
     
  block_blob_service = BlockBlobService(account_name=storage_account, account_key=account_key)
  block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

  return render_template("upload.html")
  
@app.route('/listcont')
def listcont():

  block_blob_service = BlockBlobService(account_name=storage_account, account_key=account_key)
  list = block_blob_service.list_blobs(container_name)
  return render_template("listcont.html",container=container_name,list=list)  

if __name__ == '__main__':
  app.run()
