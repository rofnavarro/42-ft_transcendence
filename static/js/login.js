function signIn() {
	const clientId = 'u-s4t2ud-8f27195d382f73d94ea5d7e64c51b252415d04193021f50fa3ff713e60afb48b';
	const scope = 'public profile forum';
	const redirectUri = 'https://httpbin.org/anything';

	const authUrl = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code`;

	window.location.href = authUrl;
}