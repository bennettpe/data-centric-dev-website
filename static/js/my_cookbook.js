//Add ingredients form
$('.more-ingredients').click(function () {
    addIngredients();
    return false; //Stops page jumping back to top
})

function addIngredients() {
    var option = `<div class="ing-del">
                    <input type="text" class="form-control mb-2 mr-2" id="ingredient" name="recipe_ingredient" placeholder="Input ingredient" />
                    <span class="delete">
                        <i class="fas fa-times-circle"></i> Del 
                    </span>
                </div>`;
    $(option).insertBefore('.list-more-ingredients');
}

// Remove ingredients form
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
    var option = `<div class="ing-del">
                    <textarea class="form-control mb-2 ml-2" id="method" rows="2" name="recipe_method" placeholder="Input instructions"></textarea>
                    <span class="delete">
                        <i class="fas fa-times-circle"></i> Del 
                    </span>
                </div>`;
    $(option).insertBefore('.list-more-instructions');
}

// Remove Instructions from form
$('.instructions-list').on('click', 'span', function () {
    var rem = $(this).closest('div.ing-del');
    $(rem).remove();
});