$(document).ready(function () {
    let form = $('#add-to-basket-form');
    calculation_total_order_amount();

    form.on("submit", function (e) {
        e.preventDefault();
        let number = $("#number").val();
        let submit_btn = $("#submit_btn");
        let product_id = submit_btn.data("product_id");
        let product_name = submit_btn.data("product_name");
        let product_price = submit_btn.data("product_price");
        let csrf_token =  $('#add-to-basket-form [name="csrfmiddlewaretoken"]').val();
        let url = form.attr("action");

        let data = {};

        data.product_id = product_id;
        data.product_name = product_name;
        data.product_price = product_price;
        data.number = number;
        data.csrfmiddlewaretoken = csrf_token;

        $.ajax({
            url:url,
            type:'POST',
            data:data,
            cache:true,
            success:function(data){
                $('#basket-is-empty').remove();
                $('.product-in-basket-container').remove();
                data.products_in_basket.forEach((element) => {
                    $('#shopping-list').append('<div class="product-in-basket-container"><li class="product-in-basket" id="' + element.product_id + '">' + element.name + ' ' + element.count + ' шт * ' + element.price + ' за шт = ' + element.count * element.price + '</li></div>');
                });
            },
            error: function () {
                console.log("Error!");
            }
        });
    });

    let basket_container = document.getElementById("basket-container");

    basket_container.onmouseover = function () {
        let basket = document.getElementById("basket");
        basket.style.display = "flex";
    }

    basket_container.onmouseout = function () {
        let basket = document.getElementById("basket");
        basket.style.display = "none";
    }

    let basket_toggler = document.getElementById("basket-toggler");

    basket_toggler.onmousedown = function () {
        let basket = document.getElementById("basket");
        if (basket.style.display === "flex"){
            basket.style.display = "none";
        }
        else {
            basket.style.display = "flex";
        }
    }

    function calculation_total_order_amount(){
        let total_order_amount = 0;
        $('.total-amount').each(function () {
            total_order_amount += parseFloat($(this).text());
        });
        $('#total-order-amount').text(total_order_amount);
    }

    $(document).on("change", ".count", function () {
        let current_row_count = $(this).val();
        console.log(current_row_count);
        let current_tr = $(this).closest('tr');
        let current_price = parseFloat(current_tr.find(".price-per-item").text());
        let total_amount = current_row_count * current_price;
        current_tr.find('.total-amount').text(total_amount);
        calculation_total_order_amount();
    });
});