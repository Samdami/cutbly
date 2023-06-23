// const form = document.querySelector('form');
// form.addEventListener('submit', async (event) => {
//   event.preventDefault();
//   const urlInput = form.elements.url;
//   const url = urlInput.value;
//   const response = await fetch('/shorten_url', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ url })
//   });
//   const data = await response.json();
//   const shortUrl = window.location.href + data.short_id;
//   const resultContainer = document.createElement('div');
//   resultContainer.innerHTML = `
//     <p>Your shortened URL:</p>
//     <a href="${shortUrl}">${shortUrl}</a>
//   `;
//   form.after(resultContainer);
// });

// // Fetch the Swagger JSON file using Axios
// axios.get('/api/v1/swagger.json')
//   .then(function (response) {
//     // Create a Swagger UI instance with the fetched JSON
//     const ui = SwaggerUIBundle({
//       spec: response.data,
//       dom_id: '#swagger-ui',
//       deepLinking: true,
//       presets: [SwaggerUIBundle.presets.apis],
//       plugins: [SwaggerUIBundle.plugins.DownloadUrl],
//       layout: 'StandaloneLayout',
//     });
//   })
//   .catch(function (error) {
//     console.error('Failed to fetch Swagger JSON:', error);
//   });


axios.get('https://scissiorapi.onrender.com/api/v1/swagger.json')
  .then(response => {
    const swaggerJson = response.data;
    const swaggerUI = SwaggerUIBundle({
      spec: swaggerJson,
      dom_id: '#swagger',
      presets: [SwaggerUIBundle.presets.apis],
      plugins: [SwaggerUIBundle.plugins.DownloadUrl],
    });
  })
  .catch(error => {
    console.error('Error loading Swagger JSON:', error);
  });

