$ ->
  window.ranker = "OkapiBM25"
  set_ranker_callbacks()
  $(".input-group").keypress (k) ->
    if k.which == 13 # enter key pressed
      $("#search_button").click()
      return false;
  $("#search_button").click -> do_search()

do_search = () ->
  query = $("#query_text").val()
  if query.length != 0
    $("#search_results_list").empty()
    $.ajax "search-api",
      type: "POST"
      contentType: "application/json; charset=utf-8"
      dataType: "json"
      data: JSON.stringify
        query: query
        ranker: window.ranker
      success: (data, stat, xhr) -> print_results data
      failure: (axhr, stat, err) ->
        $("#search_results_list").append("<li>Something bad happened!</li>")

set_ranker_callbacks = () ->
  $("#OkapiBM25").click ->
    window.ranker = "OkapiBM25"
    $("#search_concept").text("Okapi BM25")
    do_search()
  $("#PivotedLength").click ->
    window.ranker = "PivotedLength"
    $("#search_concept").text("Pivoted Length")
    do_search()
  $("#DirichletPrior").click ->
    window.ranker = "DirichletPrior"
    $("#search_concept").text("Dirichlet Prior")
    do_search()
  $("#JelinekMercer").click ->
    window.ranker = "JelinekMercer"
    $("#search_concept").text("Jelinek-Mercer")
    do_search()
  $("#AbsoluteDiscount").click ->
    window.ranker = "AbsoluteDiscount"
    $("#search_concept").text("Absolute Discount")
    do_search()

print_results = (result) ->
  console.log result.results
  if result.results.length == 0
    $("#search_results_list").append('<p>No results found!</p>')
    return
  displayed = 0
  for doc in result.results
    break if displayed == 20
    continue if (doc.path.includes ":") or (doc.path.length > 60)
    displayed += 1
    path = doc.path.replace(/_/g, " ")
    html = "<li style = 'height:200px;margin-bottom:50px;'> <div style='margin-top:-10px'> <a href='http://www.imdb.com/title/#{doc.path}' style='text-decoration : none' target='_blank'> <div style = 'height:170px;float:left;margin-right: 50px; display: inline-block;'>  <h4 style='margin-top:-0.5px'>#{doc.name}</h4> <p style='font-size:16px;max-width: 400px;'> <img src='./image/star.png' alt='Rating' style='width:30px;height:30px;'> #{doc.rating} &nbsp;| #{doc.time} <em style='float:right'> #{doc.genre}</em></br>#{doc.title} </br> </p> </div> <div style = 'height:170px;float:right;margin-right: 50px; display: inline-block;'> <img src='./image/#{doc.namestrip}.jpg' alt='' style='width:150px;height:180px;'> </div> </div> </a> </li>"
    $("#search_results_list").append(html)
