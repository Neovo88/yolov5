var readytosend = false

window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		input = $('#imageinput')[0]
		if(readytosend)
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			$.ajax({
				url: "http://localhost:5000/detectObject", // fix this to your liking
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					console.log(data);
					bytestring = data['status']
					image = bytestring.split('\'')[1]
					imagebox.attr('src' , 'data:image/jpeg;base64,'+image)
				}
			});
		}
	});
};

function readUrl(input){
	imagebox = $('#imagebox')
	console.log("evoked readUrl")
	console.log(input.files)
	if(input.files && input.files[0]){
		filename = input.files[0].name.split(".")
		if(filename[1] == "jpg" || filename == "png"){
			let reader = new FileReader();
		    reader.onload = function(e){
			console.log(e)
			imagebox.attr('src',e.target.result); 
			}
			reader.readAsDataURL(input.files[0]);
			readytosend = true
		}else{
			console.log("error")
			readytosend = false
		}
	}	
}