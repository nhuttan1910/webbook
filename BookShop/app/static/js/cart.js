function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    })
}

function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'quantity': obj.value
        }),  headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        obj.disabled = false;
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity

        let n = document.getElementsByClassName('cart-amount');
            for (let m of n)
                m.innerText = data.total_amount;

        

    });
}

function deleteCart(id, obj) {
    if (confirm("Ban chac chan xoa khong?") == true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            obj.disabled = false;
            let c = document.getElementsByClassName('cart-counter');
            for (let d of c)
                d.innerText = data.total_quantity

            let n = document.getElementsByClassName('cart-amount');
            for (let m of n)
                m.innerText = data.total_amount;

            let r = document.getElementById(`sach${id}`);
            location.reload();
            r.style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn có chắc chắn muốn thanh toán!") === true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                window.location.href = '/cart';
            else
                alert(data.err_msg);
        })
    }
}

function pay_online() {
    if (confirm("Bạn có chắc chắn muốn thanh toán!") === true) {
        fetch('/api/pay_online', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                window.location.href = '/cart';
            else
                alert(data.err_msg);
        })
    }
}
