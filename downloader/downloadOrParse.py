
# http://www.melbournefringe.com.au/fringe-festival
# http://www.melbournefringe.com.au/fringe-festival?page=40


DOWNLOAD_URL = "http://www.melbournefringe.com.au/fringe-festival?page=" 
DOWNLOAD_URL_SUFFIX = ""
OUTPUT_DIR = "source/pages/"
OUTPUT_EVENT_LIST = OUTPUT_DIR + "data_list.js"
OUTPUT_PAGES = OUTPUT_DIR + "p" 
OUTPUT_PAGES_SUFFIX = ".html"
OUTPUT_EVENT = OUTPUT_DIR + "e" 
OUTPUT_EVENT_SUFFIX = ".html"




class WebPage:
	def __init__(self,url):
		self.url = url;
	def download(self):
		import urllib
		f = urllib.urlopen(self.url)
		self.contents = f.read()
		f.close()
		return self.contents
	def read(self):
		f = open(self.url)
		self.contents = f.read()
		f.close()
		return self.contents
	def save(self, output):
		f = open(output, 'w')
		f.write(self.contents)
		f.close()
	def data(self):
		return self.contents;

def download(url, output):
	page = WebPage("")
	page.url = url
	print page.url 
	print "Downloading...."
	page.download()
	print len(page.contents)
	page.save(output)

def downloadAllList():
	for i in range(1,37):
		download("%s%s%s" % (DOWNLOAD_URL, i, DOWNLOAD_URL_SUFFIX), "%s%s%s" % (OUTPUT_PAGES, i, OUTPUT_PAGES_SUFFIX))
	parseAllListPagesDownloadAllShows();

def findRegex(regx_pattern, content, flags=""):
	import re
	if flags == "" :
		pattern = re.compile(regx_pattern)
	else :
		pattern = re.compile(regx_pattern, flags)
	match  = re.search(pattern, content)
	if match : 
		return match.group(1)
	return ""
def findRegexAll(regx_pattern, content, flags=""):
	import re
	if flags == "" :
		pattern = re.compile(regx_pattern)
	else :
		pattern = re.compile(regx_pattern, flags)
	match  = re.findall(pattern, content)
	if match : 
		return match
	return ""

def extractEventDetailsFromList(contents):
	# <div class="fatcol">
	# 	<div class="imagewrap">
	# 		<a href="http://www.melbournefringe.com.au/fringe-festival/show/12-days-of-central-laughs/" class="image">
	#         	<img src="http://www.melbournefringe.com.au/thumbnails/show/228x95/402.jpg" alt="Image of 12 Days of Central Laughs" width="228" height="95" />
	# 		</a>

	# 					<div class="categoryHanger cleartext comedy">Comedy</div>
	# 			</div>

	# 	<div class='suggestion-mask' data-href="http://www.melbournefringe.com.au/fringe-festival/show/12-days-of-central-laughs/" style="display:none;">
	#     	<a  href="http://www.melbournefringe.com.au/fringe-festival/show/12-days-of-central-laughs/"  class='mask'></a>
	#         <span class='title'>Add To Playlist</span>
	#         <a class='plus ajax cboxElement show-dialog-actions' href="http://www.melbournefringe.com.au/itinerary/modal/?sid=402&format=html"></a>
	# 	</div>

	# 	<h4><a href="http://www.melbournefringe.com.au/fringe-festival/show/12-days-of-central-laughs/">12 Days of Central Laughs</a></h4>
	# </div>

	link = ""
	title = ""
	image = ""
	category = ""
	brief = ""

	link_and_title = findContent(contents, "<h4", "</h4>")
	import re


	link = findContent(link_and_title, "href=\"", "\">")
	# print link_and_title

	pattern = re.compile("src=['\"](.*)['\"]")
	match  = re.search(pattern, link_and_title)
	if match : 
		image = match.group(1)


	link = findRegex("<a href=['\"](.*)['\"]", link_and_title)
	title = findRegex("<a[^>]+>([^<]+)<", link_and_title)
	image = findRegex("src=['\"]([^\"]+)['\"]", contents)
	category = findRegex("class=\"categoryHanger cleartext (.+)\"", contents)
	return {
		"link": link
		, "title" : title
		, "image" : image
		, "category" : category
		, "brief" : brief
	}	
	
def findEventInListStart(contents, start_pos):
	pos_1 = contents.find("<div class=\"fatcol\"",start_pos)
	pos_2 = contents.find("<div class=\"fatcol ",start_pos)
	if pos_1 < pos_2 and pos_1 != -1:
		return pos_1
	else :
		return pos_2
def findEventInListEnd(contents, start_pos):
	pos = findEventInListStart(contents, start_pos)
	if pos == -1 :
		pos = contents.find("<div class=\"clr",start_pos)
	return pos;
def findContent(contents, start_text, end_text, include_start_tag=True, include_end_tag=True):
	# link and name
	pos_start_with_start_text = contents.find(start_text)
	pos_end_without_end_text = contents.find(end_text, pos_start_with_start_text+1)
	pos_start = pos_start_with_start_text
	if not include_start_tag :
		pos_start += len(start_text)
	pos_end = pos_end_without_end_text
	if include_end_tag :
		pos_end += len(end_text)
	return contents[pos_start:pos_end]

def parseListPageAndDownloadShows(pageNo, pageLocation):
	#print "Parsing list page %s in %s" % (pageNo, pageLocation)	
	f = open(pageLocation)
	contents = f.read()
	f.close()
	start = 0
	count = 0
	while True : 
		event_start = findEventInListStart(contents, start)
		if event_start == -1 :
			break
		else : 
			event_end = findEventInListEnd(contents, event_start+1)
			if event_end == -1 :
				print("Hmmmm no end? Starts at %s" % event_start)
			else : 
				count += 1
				eventDetails = extractEventDetailsFromList(contents[event_start:event_end])
				download("%s" % eventDetails["link"], "%s%s_%s%s" % (OUTPUT_EVENT, pageNo, count, OUTPUT_EVENT_SUFFIX))

			start = event_start+1
	print "Found %s items on page %s" % (count, pageNo)



def parseDetailPage(pageLocation):
	#print "Parsing detail page %s" % (pageLocation)	
	f = open(pageLocation)
	contents = f.read()
	f.close()

# <div class="innerleft show-details">
#                 <h4 class="label-center" style="position:relative;">September/October<span id="ticketLdr" style="position:absolute; height:32px; width:32px; left:184px; top:-14px;"></span></h4>
#                 <table cellpadding="0" cellspacing="0" width="100%" class="calendar borderbottom">
# 	<thead>
#     	<tr>
#         	<th class="weekend">S</th>
#             <th class="weekday">M</th>
#             <th class="weekday">T</th>
#             <th class="weekday">W</th>
#             <th class="weekday">T</th>
#             <th class="weekday">F</th>
#             <th class="weekend">S</th>
#     	</tr>
# 	</thead>
# 	<tbody>
# 	<tr class="even">
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td><span class="calendar-day festival-date">18</span>
# </td>
# 		<td><span class="calendar-day festival-date">19</span>
# </td>
# 		<td><span class="calendar-day festival-date">20</span>
# </td>
# 		<td><span class="calendar-day festival-date">21</span>
# </td>
# 	</tr><tr class="odd">
# 		<td><span class="calendar-day festival-date">22</span>
# </td>
# 		<td><span class="calendar-day festival-date">23</span>
# </td>
# 		<td><span class="calendar-day festival-date">24</span>
# </td>
# 		<td><span class="calendar-day festival-date">25</span>
# </td>
# 		<td><span class="calendar-day festival-date">26</span>
# </td>
# 		<td><span class="calendar-day festival-date">27</span>
# </td>
# 		<td><span class="calendar-day festival-date">28</span>
# </td>
# 	</tr><tr class="even">
# 		<td><span class="calendar-day festival-date">29</span>
# </td>
# 		<td><span class="calendar-day festival-date">30</span>
# </td>
# 		<td><span class="calendar-day festival-date show-active">1</span>
# </td>
# 		<td><span class="calendar-day festival-date show-active">2</span>
# </td>
# 		<td><span class="calendar-day festival-date show-active">3</span>
# </td>
# 		<td><span class="calendar-day festival-date show-active">4</span>
# </td>
# 		<td><span class="calendar-day festival-date show-active">5</span>
# </td>
# 	</tr><tr class="odd">
# 		<td><span class="calendar-day festival-date">6</span>
# </td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 		<td>&nbsp;</td>
# 	</tr>	</tbody>
#     <tfoot>
#         <tr>
#             <td colspan="3" class="cal-soldout"><span></span>Sold out</td>
#             <td colspan="4" class="cal-cancelled"><span></span>Cancelled</td>
#         </tr>
#     </tfoot>
# </table>

#                                     <h4>Time</h4>
#                     <p>9.15pm, Sat 3.30pm &amp; 9.15pm (60min)</p>
                
#                                     <h4>Tickets</h4>
#                                                 <p>Full Price: $20.00<br>Concession: $16.00<br>Tuesday: $15.00</p>
                                    
#                 <div class="show-collapsable" style="">
#                     <h4>Venue</h4>

# <h5>Gasworks - Theatre</h5>

# <p>21 Graham St<br>Albert Park</p>

# 	<p>
# 		<a class="location-link cBoxElement ajax shadowbox" href="http://www.melbournefringe.com.au/venue/map/gasworks-theatre/?modal=true" rel="shadowbox;height=500;width=600">Location Map</a>
# 	</p>

# <p>
# 	<img src="http://www.melbournefringe.com.au/img/icon-drink.gif" alt="Drinks Available">    <img src="http://www.melbournefringe.com.au/img/icon-food.gif" alt="Food Available">    <img src="http://www.melbournefringe.com.au/img/icon-wheelchair.gif" alt="Wheelchair Accessible"></p>

# <h4>Transport</h4>

# 				<p>Tram: 1<br>Stop: 31</p>
# 				<p>Melways: 2J G7</p>
	

#                     <h4>Category</h4>
#                     <p>Circus</p>

#                                     </div>
#                 <a href="#" class="show-collapsable-toggle open"><span></span>Show location info</a>

#             </div>

#                 <div class="showinfo">
#            </div> # extra diff need to remove
#            <div class="clr"> </div>
#############################################################
# <div class="innerright">
#                                 <div class="category-location">
#                                         <div class="category-bubble">
#                         <div class="bubble">
#                             <span class="circus"></span>
#                         </div>
#                         <a href="http://www.melbournefringe.com.au/fringe-festival/browse/circus">
#                             Circus                        </a>
#                     </div>
#                                         <div class="venue-bubbles">
#                         <div class="venue-bubble">
#                             <div class="bubble"></div>
#                             <p><a href="http://www.melbournefringe.com.au/venue/map/gasworks-theatre/?modal=true" rel="shadowbox;height=500;width=600">Gasworks - Theatre</a>                            </p>
#                         </div>
#                     </div>
#                                     </div>
#                 <div class="showinfo">

                    
#                     <p>A physical comedy based in an office space. Imagine two cogs in the machine of an unknown corporation, whose lives are stuck in a rut and composed completely of daily routine. These two go about their day procrastinating and in the end have accomplished only the most mundane of tasks. But suddenly when their routine is broken, chaos ensues.</p><p>Merging circus and contemporary clowning and with direction from award winning circus performer Avan Whaite, <em>...We Should Quit</em> incorporates traditional circus acts such as Chinese pole, corde lisse, acrobatics and happy cook skills, in a way which allows normal and abnormal to become interchangable.</p>
                                            
#                         <p><a href="http://afterdarktheatre.com" target="_new">afterdarktheatre.com</a></p>
                    
#                                             <p><strong>Created and Performed by</strong> Tom and Morgan</p>
                    
#                                             <p><strong>Directed by</strong> Avan Whaite</p>
#                                         <div class="show-social-media">
#                         <div class="fb-like" data-send="false" data-layout="button_count" data-width="60" data-show-faces="false"></div>
#                         <a href="https://twitter.com/share" class="twitter-share-button" data-count="none">Tweet</a>
#                         <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
#                     </div>
#                 </div>
#             </div>
###########################

	info = ""
	category = ""
	venue_name = ""
	venue_address = ""
	venue_link = ""
	venue_transport = ""
	venue_facilities = ""
	dates = []
	time_raw = [3,4,{"a":1}]
	ticket = [1,2]
	image = ""
	name = ""
	description = ""

	feature_section = contents[contents.find("<div id=\"feature-panel\">")+1:len(contents)]

	name = findRegex("<span>(.*)</span>", feature_section)
	description = findRegex("(.*)</div>", feature_section).strip()
	if description.find("carousel-wrapper") != -1 :
		description = ""
	image = findRegex("img.*src=[\"'](.*?)[\"']",feature_section)
	link = findRegex("og:url[\"'] content=[\"'](.*?)[\"']",contents).replace("/browse/", "/show/")

	time_raw = findRegex("<p>(.*)</p>", contents[contents.find("<h4>Time</h4>")+1:len(contents)])
	ticket_raw = findRegex("<p>(.*)</p>", contents[contents.find("<h4>Tickets</h4>")+1:len(contents)])
	ticket = ticket_raw
	ticket = {}
	ticket["raw"] = ticket_raw;
	ticket["full"] = ""
	ticket["concession"] = ""
	ticket["group"] = ""
	ticket["other"] = ""

	ticket_filter = {
		"full": "Full"  
		,"concession": "Concession"  
		,"free": "This show is free" 
		,"donation": "This show is by donation" 
		,"preview": "Preview" 
		,"group": "Group" 
		,"tuesday": "Tuesday"
		}
	tickets_found = {}	
	tickets_found2 = {}

	group = False
	for line in ticket_raw.split("<br />") : 
		found = False
		for key,text in ticket_filter.iteritems() :
			if line.find(text) == 0 :
				tickets_found2[key] = line
				group  = (key == "group")
				found = True
				break
		if found == False :
			if group == True :
				tickets_found2["group_extra"] = line
				group = False
			else :
				if line.find("$") != -1 :
					if "ticket_other" not in tickets_found2 :
						tickets_found2["ticket_other"] = []
					tickets_found2["ticket_other"].append(line);
				else :
					print "1: " + link
					print "1: " + line

	# print contents
	dates = {}
	dates["active"] = findRegexAll("show-active(?:[\"']| )[.*]?>(.*?)</span>", contents, "")
	dates["sold_out"] = findRegexAll("show-soldout(?:[\"']| )[.*]?>(.*?)</span>", contents, "")
	dates["cancelled"] = findRegexAll("show-cancelled(?:[\"']| )[.*]?>(.*?)</span>", contents, "")
	dates["all"] = []
	for i in range(0,len(dates["active"])):
		dates["all"].append(dates["active"][i])
	for i in range(0,len(dates["sold_out"])):
		dates["all"].append(dates["sold_out"][i])


	venue_section = contents[contents.find("<h4>Venue</h4>")+1:len(contents)]
	import re
	
	venue = {}

	venue["name"] = findRegex("<h5>(.*)</h5>", venue_section)
	venue["address"] = findRegex("<p>(.*)</p>", venue_section)
	venue["map_link"] = findRegex("<a.*href=\"(.*)\"", venue_section)
	venue["transport"] = findRegex("<h4>Transport</h4>(.*?)<h4>", venue_section, re.DOTALL)
	venue["facilities"] = findRegex("<p>.*?(<img.*?)</p>.*?<h4>Transport</h4>", venue_section, re.DOTALL)

#	print venue

	category = findRegex("<p>(.*)</p>", contents[contents.find("<h4>Category</h4>")+1:len(contents)])
	link = findRegex("og:url[\"'] content=[\"'](.*?)[\"']",contents).replace("/browse/", "/show/")
	info = findRegex("<div class=\"showinfo\">(.*?)<div class=[\"']show-social-media[\"']>",contents, re.DOTALL).strip()

	data = {
		"name" : name
		 , "description": description
		 , "link" : link
		 , "dates": dates
		 , "time" : time_raw	
		 , "ticket" : tickets_found2
		, "venue" : venue
		, "dates" : dates
		 , "image" : image
		 , "category" : category
		 , "info" : info
	}	
	# print data
	return data


	print pageLocation

def parseAllListPagesDownloadAllShows():
	i = 0
	while True :
		import os
		i+=1
		path_to_file = ("%s%s%s" % (OUTPUT_PAGES, i, OUTPUT_PAGES_SUFFIX))
		if os.path.isfile(path_to_file) :
			print i
			parseListPageAndDownloadShows(i, path_to_file)
		else :
			break
def parseAllDetailPages():

	print "Saving to %s" % OUTPUT_EVENT_LIST
	f = open(OUTPUT_EVENT_LIST, 'w')
	f.write("data_list = [{}");

	pageNo = 1
	itemNo = 1
	while True :
		import os
		path_to_file = ("%s%s_%s%s" % (OUTPUT_EVENT, pageNo, itemNo, OUTPUT_EVENT_SUFFIX))
		if os.path.isfile(path_to_file) :
			details = parseDetailPage(path_to_file)
			print "%s %s" % (pageNo, itemNo)
			f.write(",%s\n" % details);
			itemNo += 1
		else :
			if not itemNo == 1 :
				pageNo += 1
				itemNo = 1
			else :
				break
	f.write("];");
	f.close()


events = {}
venues = {}
venue_names = {}
venue_names_dup = {}
from sys import argv

try:   
	script, mode = argv
	print mode
	if mode == "download" :
		downloadAllList() # download all main pages and show pages
	elif mode == "parse" :
		parseAllDetailPages() # parses all details pages and output json
	else :
		print "Unrecognized mode: %s" % (mode)
		print "Specify mode: download or parse"
except Exception, e:
	print e

#downloadAllList() # download all main pages and show pages
#parseAllDetailPages() # parses all details pages and output json