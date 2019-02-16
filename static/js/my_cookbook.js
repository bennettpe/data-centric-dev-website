// Add extra Ingredient inputs to add recipe form
$('.more-ingredients').click(function () {
    addIngredients();
    return false; //Stops page jumping back to top
})

function addIngredients() {
    var option = '<div class="ing-del"> <input type="text" class="form-control mb-2" id="inputMainingredient" placeholder="Ingredient" /> <span class="delete"> X </span> </div>';
    $(option).insertBefore('.list-more-ingredients');
}

// Remove Ingredients from form
$('.ingredients-list').on('click', 'span', function () {
    var rem = $(this).closest('div.ing-del');
    $(rem).remove();
});


// Add extra Instruction inputs to add recipe form
$('.more-instructions').click(function () {
    addInstructions();
    return false; //Stops page jumping back to top
})

function addInstructions() {
    var option = '<div class="ing-del"> <textarea class="input form-control mb-2" id="inputInstructions1" rows="2" placeholder="Instructions"></textarea> <span class="delete"> X </span> </div>';
    $(option).insertBefore('.list-more-instructions');
}

// Remove Instructions from form
$('.instructions-list').on('click', 'span', function () {
    var rem = $(this).closest('div.ing-del');
    $(rem).remove();
});