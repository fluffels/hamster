/*
 *Calls the modal for choosing an aggregator and send the following data:
 *agg_name : String      the name of the aggregator the current assessment is using
 *numC : Int        the number of children the assessment has
 *assess_id : Int   the assessment id of the assessment as specified in the db
 *children : Array  an array containing information about children of the assessment
 */
$(document).on("click", ".open-aggregation-modal", function () {
     var agg_name = $(this).data('agg_name');
     var numC = $(this).data('numC');
     var children_arr = $(this).data('children_of_ass');
     var assess_id = $(this).data('assess_id');
     $(".modal-body #agg_name").val( agg_name );
     $(".modal-body #numC").val( numC );
     $(".modal-body #assess_id").val( assess_id );
     //$(".modal-body #children").val( children );
     alert(children_arr);
     
     //Looping through children var then displaying results in html page
     for (var i = 0 ; i < children_arr.length ; i++) {
          //Find div where you should put the form group
          //in and loop through it appending the data down there
          
          $(".modal-body #child_form_group_id").get(0).innerHTML =
          '<div class="form-group">\
               <label class="col-sm-3 control-label" for="weightedSumAssessment">Assign weight</label>\
               <div class="col-sm-5 show_children_of_assessment_agg">\
                    <input class="form-control" type="text" id="child_weight"\
                    name="child_weight" placeholder="Weight of assessment" >\
                    <input type="text" id="child_id" name="child_id" hidden="hidden" value=' + children_arr[i] + '>\
               </div>\
          </div>'
     }
     /*
       <div class="form-group">
          <label class="col-sm-3 control-label" for="weightedSumAssessment"></label>
          <div class="col-sm-5 show_children_of_assessment_agg">
                  <input class="form-control" type="text" id="child_weight" name="child_weight" placeholder="Weight of assessment" >
                  <input type="text" id="child_id" name="child_id" hidden="hidden" value="" >
          </div>
       </div>
    */
});