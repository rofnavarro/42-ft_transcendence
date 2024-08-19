
document.addEventListener('DOMContentLoaded', (event) =>
{
	const	menu_button = document.getElementById('menu-button');
	const	menu_modal = document.getElementById('menu-modal');
	const	close_button = document.getElementById('close-button');

	menu_button.addEventListener('click', () =>
	{
		menu_modal.style.display = 'block';
	});
	close_button.addEventListener('click', () =>
	{
		menu_modal.style.display = 'none';
	});
	window.addEventListener('click', (event) =>
	{
		if (event.target == menu_modal)
		{
			menu_modal.style.display = 'none';
		}
	});
});