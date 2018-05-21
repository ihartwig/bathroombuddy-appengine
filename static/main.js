var UPDATE_INTERVAL = 10000; // ms


// ui fn to submit review
function do_review(event) {
  $.post({
    url: '/update/stallrating',
    data: event.data,
    success: update_reviews
  });
}


// ui fn to hide splash
function do_hide_splash() {
  $("#splash").addClass('splash-done');
};


// convert true/false busy to UI string
function busy_to_string(busy) {
  if(busy) {
    return "Busy";
  } else {
    return "Free";
  }
}

// convert time in sec to relative time string
function update_time_to_string(time) {
  sec_in_min = 60;
  min_in_hour = 60;
  ret_time_int = time;
  ret_time_unit = "second";
  ret_time_str = "";
  // try to reduce to min
  if(ret_time_int >= sec_in_min) {
    ret_time_int = Math.floor(ret_time_int/sec_in_min);
    ret_time_unit = "minute"
  }
  // try to reduce to hour
  if(ret_time_int >= min_in_hour) {
    ret_time_int = Math.floor(ret_time_int/min_in_hour);
    ret_time_unit = "hour"
  }
  // concat and pluralize
  if(ret_time_int == 1) {
    ret_time_str = ret_time_int + " " + ret_time_unit + " ago";
  } else {
    ret_time_str = ret_time_int + " " + ret_time_unit + "s ago";
  }
  return ret_time_str;
}

// convert review avg 
function review_avg_to_elems(location, review_avg) {
  num_stars = 5;
  review_avg_int = Math.round(review_avg);

  // make base elements
  stars_elem = $("<span></span>".repeat(num_stars));
  stars_elem.each(function(i){
    // set right number of stars... in backwards order
    // debugger
    if(review_avg_int < (num_stars-i)) {
      $(this).html("&#x2606;"); // empty star
    } else {
      $(this).html("&#x2605;"); // filled star
    }
    // add form submission info from fake form
    form_elem = $("<form></form>")
      .add("<input type='text' name='location' value='"+location+"' />")
      .add("<input type='text' name='review' value='"+(5-i)+"' />")
      .add("<input type='text' name='postkey' value='asdfasdfasdfasdf' />")
    $(this).click(form_elem.serialize(), do_review); // pass form as event data
  });

  return stars_elem;
}


// call regularly to update stall status
function update_stalls_worker() {
  $.ajax({
    url: '/get/stallslatest', 
    success: function(data) {
      // console.log(data);
      $.each(data, function(location, stall) {
        list_elem = $("#"+location+"-list");
        map_elem = list_div = $("#"+location+"-map");
        // update text
        list_elem.find(".room-list-status .room-list-status-text").html(busy_to_string(stall.busy));
        list_elem.find(".room-list-status .room-list-status-time").html(update_time_to_string(stall.since_update_time));
        // update styles
        list_elem.removeClass("room-free room-busy");
        map_elem.removeClass("room-free room-busy");
        if(stall.busy) {
          list_elem.addClass("room-busy");
          map_elem.addClass("room-busy");
        } else {
          list_elem.addClass("room-free");
          map_elem.addClass("room-free");
        }
      })
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(update_stalls_worker, UPDATE_INTERVAL);
    }
  });
};


// call on-demand to update all reviews (load, review submission)
function update_reviews() {
  $.ajax({
    url: '/get/stallsreview', 
    success: function(data) {
      console.log(data)
      $.each(data, function(location, review_avg) {
        list_elem = $("#"+location+"-list");
        list_elem.find(".room-list-info .room-list-review").html(
          review_avg_to_elems(location, review_avg)
        );
      });
    }
  });
}


// setup script-dom bindings
$( document ).ready(function() {
  $("#splash").click(do_hide_splash);
  update_stalls_worker();
  update_reviews();
});

