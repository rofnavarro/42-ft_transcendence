async function loadPage(page) {
	try {
		const response = await fetch(page);
		const content = await response.text();

		const container = document.getElementById('container');
		container.innerHTML = resultPage;
	}
	catch (error) {
		console.error('Error loading page: ', error);
	}
	return container;
}

function dynamicContent(resultPage) {
	switch (resultPage) {
		case 'home':
			loadPage('home.html');
	}
}