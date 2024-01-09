function addToViewtt(id, name, price){
    alert('Scan Success')

    fetch('/api/nvcart',{
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.info(res)
        return res.json();
    }).then(function(data){
        console.info(data);
    }).catch(function(err){
        console.error(err);
    })
    location.reload();
}

function pay_nv() {
    if (confirm("Bạn có chắc chắn muốn thanh toán!") === true) {
        fetch('/api/pay_nv', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                window.location.href = '/nv/create';
            else
                alert(data.err_msg);
        })
    }
}