		/*
		Object {category: "Circus", info: "<p>A physical comedy based in an office space. Ima…  <p><strong>Directed by</strong> Avan Whaite</p>", dates: Object, link: "http://www.melbournefringe.com.au/fringe-festival/browse/we-should-quit", name: "...we should quit"…}
		category: "Circus"
		dates: Object
		active: Array[5]
		all: Array[5]
		cancelled: ""
		sold_out: ""
		__proto__: Object
		description: "A Circus of Errors"
		image: "http://www.melbournefringe.com.au/thumbnails/show/720/216.jpg"
		info: "<p>A physical comedy based in an office space. Imagine two cogs in the machine of an unknown corporation, whose lives are stuck in a rut and composed completely of daily routine. These two go about their day procrastinating and in the end have accomplished only the most mundane of tasks. But suddenly when their routine is broken, chaos ensues.</p><p>Merging circus and contemporary clowning and with direction from award winning circus performer Avan Whaite, <em>...We Should Quit</em> incorporates traditional circus acts such as Chinese pole, corde lisse, acrobatics and happy cook skills, in a way which allows normal and abnormal to become interchangable.</p>

		↵                                            

		↵                        <p><a href="http://afterdarktheatre.com" target="_new">afterdarktheatre.com</a></p>

		↵                    

		↵                                            <p><strong>Created and Performed by</strong> Tom and Morgan</p>

		↵                    

		↵                                            <p><strong>Directed by</strong> Avan Whaite</p>"
		link: "http://www.melbournefringe.com.au/fringe-festival/browse/we-should-quit"
		name: "...we should quit"
		ticket: Object
		concession: "Concession: $16.00"
		full: "Full Price: $20.00"
		tuesday: "Tuesday: $15.00"
		__proto__: Object
		time: "9.15pm, Sat 3.30pm & 9.15pm (60min)"
		venue: Object
		address: "21 Graham St<br />Albert Park"
		facilities: "<img src="http://www.melbournefringe.com.au/img/icon-drink.gif" alt="Drinks Available" />    <img src="http://www.melbournefringe.com.au/img/icon-food.gif" alt="Food Available" />    <img src="http://www.melbournefringe.com.au/img/icon-wheelchair.gif" alt="Wheelchair Accessible" />"
		map_link: "http://www.melbournefringe.com.au/venue/map/gasworks-theatre/?modal=true"
		name: "Gasworks - Theatre"
		transport: "
		↵
		↵				<p>Tram: 1<br />Stop: 31</p>
		↵				<p>Melways: 2J G7</p>
		↵	
		↵

		↵                    "
		__proto
		*/
var DEBUG = false;

	function load_list(events,append){
		if(typeof(append) == "undefined") append = false;
		if(typeof(listDetails) == "undefined") listDetails = $("#list");
		if(typeof(listDetailsTemplate) == "undefined") {
			listDetailsTemplate = Handlebars.compile($("#list-template").html()); 
		}
		// console.log("load list: " + events.length + ". append: " + append);
		if(events.length == 0){
			if(!append) listDetails.html("");
			return;
		}
		var events_data = [];
		var data = {};
		for(var i = 0; i < events.length; i++){
			var details = events[i];
			data = {};
			for(key in details){
				data[key] = details[key];
			}
			//data['dates'] = get_dates(details);
			data['tickets'] = get_tickets(details);
			events_data.push(data);
		}
		// console.log("add: " + events_data.length);
		var output = listDetailsTemplate({items: events_data});
		if(append)
			listDetails.append(output);
		else
			listDetails.html(output); 
		$("#search-results-number").text($("#list > .panel").size());
		$("#search-results").show();
	}


	function load_event(details){
		if(typeof(pageDetails) == "undefined") pageDetails = $("#details");
		if(typeof(pageDetailsTemplate) == "undefined") {
			pageDetailsTemplate = Handlebars.compile($("#details-template").html()); 
		}
		var data = {}
		for(key in details){
			data[key] = details[key];
		}
		data['dates'] = get_dates(details);
		data['tickets'] = get_tickets(details);

		pageDetails.html(pageDetailsTemplate(data)); 
	}

	function get_tickets(details){
		var tickets = "";
		if(details.ticket.full){
			if(tickets != "") tickets += "<br>";
			tickets += details.ticket.full;
		}
		if(details.ticket.concession){
			if(tickets != "") tickets += "<br>";
			tickets += details.ticket.concession;
		}
		for(key in details.ticket){
			if(key == "full") continue;
			if(key == "concession") continue;
			if(tickets != "") tickets += "<br>";
			tickets += details.ticket[key];
		}
		return tickets;
	}
	function get_dates(details){
		var dates = "";
		dates += "Active:" + details.dates.active;
		if(details.dates.sold_out)
			dates += "<br>" + "Sold out:" + details.dates.sold_out;
		if(details.dates.cancelled)
			dates += "<br>" + "Cancelled:" + details.dates.cancelled;
		return dates;
	}


	function event_match_search(event, search_terms){
		if(typeof(event) === "undefined") {
			if(DEBUG) console.log("Fail on no event");
			return false;
		}
		if(typeof(search_terms) === "undefined") return true;

		// console.log(event.category);
		if(!event.name) {
			if(DEBUG) console.log("Fail on name - no name");
			return false;
		}
		if(!search_regex(search_terms["name"], event.name)) {
			if(DEBUG) console.log("Fail on name");
			return false;
		}
		if(!search_regex(search_terms["venue"], event.venue.name)){
			if(DEBUG) console.log("Fail on venue");
			return false;
		}
		if(!search_regex(search_terms["category"], event.category)) {
			if(DEBUG) console.log("Fail on category");
			return false;
		}

		// date search
		var d = new Date();
		var dateStart = new Date();
		dateStart.setDate(18);
		dateStart.setMonth(8);
		dateStart.setFullYear(2013);
		var dateEnd = new Date();
		dateEnd.setDate(6);
		dateEnd.setMonth(9);
		dateEnd.setFullYear(2013);

		var today = "" + d.getDate();
		if(search_terms["date-end"]){
			if(!search_terms["date-start"]) search_terms["date-start"] = search_terms["date-end"];
			search_terms["date-end"] = null;
		}
		if(search_terms["today"] || search_terms["date-start"]){
			if(!event.dates){
				if(DEBUG) console.log("Fail on dates - no dates array");
				return false;
			}
			if(!event.dates.active){
				if(DEBUG) console.log("Fail on dates - no datres active");
				return false;
			}

			if(search_terms["today"]){
				if(!in_array(today+"", event.dates.active)){
					if(DEBUG) console.log("Fail on dates - not today " + today);
					return false;
				}
			}

			if(search_terms["date-end"]){
				if(!in_date_range(search_terms["date-start"],search_terms["date-end"],event.dates.active)){
					if(DEBUG) console.log("Fail on dates - not in range");
					return false;
				}
			}
			else if(search_terms["date-start"]){
				if(!in_array(search_terms["date-start"],event.dates.active)) {
					if(DEBUG) console.log("Fail on dates - not on day " + search_terms["date-start"]);
					return false;
				}
			}
		}

		// price search
		if(search_terms["price-free"])
			if(!event.ticket.free) {
				if(DEBUG) console.log("Fail on ticket - notfree");
				return false;
			}
		if(search_terms["price"]){
			if(!event.ticket.full){
				// if(search_terms["price"] < )
				if(!event.ticket.free){
					if(DEBUG) console.log("Fail on ticket - price");
					return false;
				}
			}
			else
			{
				var price = event.ticket.full.match(/\$(\d+)/gi);
				price = price[0].substring(1);
				if(parseInt(price) > parseInt(search_terms["price"])) {
					if(DEBUG) console.log("Fail on ticket - to ex " + price + " vs " + search_terms["price"]);
					return false;
				}
			}
		}
		// console.log(event.ticket)

		return true;
	}


	////////////////////////////////////////////////////////////////////////////////
	// utilities - 1
	function process_single_number_date(day){
		var date = '2013-';
		if(day > 10) // sept
			date += "08";
		else
			date += "09";
		if((day+"").length == 1) day = "0" + day;
		date += "-"+day;
		return date;
	}


	function in_array(needle, haystack){
		for(var i = 0; i < haystack.length; i++){
			if(needle == haystack[i]) return true;
		}
		return false;
	}

	function in_date_range(date_start, date_end, date_list){
		// 1,   5
		// 20,  40
		if(date_start){
			date_start = process_single_number_date(date_start);
			console.log("start: " + date_start);
			for(var i = 0; i < date_list.length; i++){
				var day = process_single_number_date(date_list[i]);
				console.log("start: " + day + " > " + date_start + " == " + (day >= date_start));
				if(day >= date_start) return true;
			}
		}
		if(date_end){
			date_end = parseInt(date_end);
			date_end = process_single_number_date(date_end);
			for(var i = 0; i < date_list.length; i++){
				var day = process_single_number_date(date_list[i]);
				console.log("end: " + day + " < " + date_end + " == " + (day <= date_end));
				if(day <= date_end) return true;
			}
		}
		return false;
	}
	function search_regex(needle,haystack){
		if(!needle) return true;
		if(needle == "") return true;
		var re = RegExp(needle,"gi");
		return re.test(haystack)
	}
	// utilities - 0
	////////////////////////////////////////////////////////////////////////////////

	


	// needed for the recursive search
	function searchMe(searchInputs,curr_index, time){
		search(searchInputs, curr_index, time);
	}
	function search(searchInputs, curr_index, time){
		if(data_time && time && time != data_time) return;
    	var search = {};
        $("#status").text("Searching " + (data_list.length - curr_index) + " events");

    	for(var i = 0; i < searchInputs.length; i++){
    		var searchInput = searchInputs[i];
    		if(searchInput.value !== ""){
    			search[searchInput.name] = searchInput.value;
    		}
    	}
    	var search_list = [];
    	if(!curr_index) {
    		curr_index = 0;
    		data_search_count = 0;
    	}
    	var MAX = 2000;
    	var MAX_PER_CALL = 50;
		// console.log("search " + curr_index);
    	var i;
		for(i = curr_index; i < data_list.length; i++){
    	 	var event = data_list[i];
    	 	// console.log(i + ". " + event.category);

    		if(event_match_search(event,search)){
    			search_list.push(event);
    			data_search_count++;
    			if(data_search_count >= MAX){ // how many items per page. to add later
    				console.log("Max!");
    				break;
    			}
    		}
    		if(i >= curr_index + MAX_PER_CALL) // number of searches before calling function again
    			break;
    	}
		load_list(search_list, (curr_index != 0));

		
		if(i < data_list.length){ // still more to search through
			if(data_search_count <= MAX){
					setTimeout(function(){ searchMe(searchInputs, curr_index+MAX_PER_CALL+1, time);}, 200);
			}
		}
		else{
			$("#status").text("Searching complete");
		}


	}

	Handlebars.registerHelper('showDates', function(datesArr) {
		if(typeof(datesArr) != "object" || typeof(datesArr.join) === "undefined") return "";
			return new Handlebars.SafeString(
			datesArr.join(", ")
		);
	});    
