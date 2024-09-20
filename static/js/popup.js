document.addEventListener("DOMContentLoaded", function() 
{
	var nicknameDisplay = document.getElementById("nickname-display");
	var popup = document.getElementById("nickname-popup");
	var closePopup = document.querySelector(".close-popup");

	nicknameDisplay.addEventListener("click", function()
	{
		popup.style.display = "block";
	});

	closePopup.addEventListener("click", function()
	{
		popup.style.display = "none";
	});

	window.addEventListener("click", function(event)
	{
		if (event.target == popup) {
			popup.style.display = "none";
		}
	});
});
