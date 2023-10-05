$(document).ready(function () {
    setTimeout(function () {
        $(".alert").fadeOut("slow", function () {
            $(this).remove();
        });
    }, 3000);
});

$(document).ready(function () {
    function toggleNewCustomerFields() {
        const isChecked = $('#new-customer-radio').is(':checked');
        $('#new-customer-fields').toggle(isChecked);
        $('#existing-customer-fields').toggle(!isChecked);
        $('#existing-customer-button').toggle(!isChecked);
        $('#new-customer-button').toggle(isChecked);
    }

    // Initial toggle state
    toggleNewCustomerFields();

    // Handle radio button change event using event delegation
    $(document).on('change', 'input[type="radio"]', function () {
        toggleNewCustomerFields();
    });
});

function releaseIP(ipId, event) {
    event.preventDefault();
    $(`#release-form-${ipId}`).submit();
}

// Handle the filter button click
$('#filterButton').click(function () {
    const startIP = $('#start_ip').val();
    const endIP = $('#end_ip').val();

    $('.ip-row').each(function () {
        const ipCell = $(this).find('.ip-address-cell');
        const ip = ipCell.text().trim();

        // Check if the IP address falls within the filter range
        if (ip >= startIP && ip <= endIP) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
});

// Show and hide the allocation modal
function showModal() {
    $('#allocation-modal').removeClass('hidden');
}

function hideModal() {
    $('#allocation-modal').addClass('hidden');
}


$(document).on('DOMContentLoaded', () => {
    const mobileMenu = $('#mobile-menu');
    const mobileMenuButton = $('#mobile-menu-button');
    const closeButton = $('.navbar-close');

    mobileMenuButton.click(() => {
        mobileMenu.toggleClass('hidden');
    });

    closeButton.click(() => {
        mobileMenu.addClass('hidden');
    });
});


const currentYear = new Date().getFullYear();

document.querySelector("#currentYear").innerHTML = currentYear;