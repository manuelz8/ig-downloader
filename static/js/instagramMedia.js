const searchForm = document.getElementById('searchForm');
const mediaContainer = document.getElementById('mediaContainer');
const processInfo = document.getElementById('processInfo');

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    mediaContainer.innerHTML = '';

    const multi_url = searchForm.urlInput.value.split(',');

    let iterator = 0;
    for (const url of multi_url) {
        processInfo.innerHTML = `Loading (${iterator}/${multi_url.length})`;
        try {
            const body = { url };
            const response = await axios.post('/get_instagram_media', body);
            const file_directory = '/' + response.data.media_url;
            displayContent(file_directory);
        } catch (error) {
            console.error(error)
            displayError(error);
        }finally{
            iterator++;
            processInfo.innerHTML = `Loading (${iterator}/${multi_url.length})`;
        }
    }

    processInfo.innerHTML = '';
});

const displayContent = (file_directory) => {
    const extension = file_directory.split('.').pop();

    const mediaTag = extension === 'mp4'
    ? `<video class="card-media" src="${file_directory}" controls></video>`
    :`<img class="card-media" src="${file_directory}">`;

    const template = `
        <div class="card">
            ${mediaTag}
            <div class="h-10 d-flex align-items-center justify-content-end px-1">
                <a id="downloaderTag" class="txt-dec-none text-white text-bold c-pointer">
                    <span class="mr-1">Download</span>
                    <i class="fa-solid fa-download"></i>
                </a>
            </div>
        </div>
    `
    mediaContainer.innerHTML += template.trim();

    const downloaderTag = document.getElementById('downloaderTag');
    downloaderTag.addEventListener('click', () => {
        downloadMedia(file_directory)
    });
}

const displayError = (error) => {
    const template = `
        <div class="card">
            <h3>
                Something went wrong.
                This profile/post has age restriction or isn't public
            </h3>
        </div>
    `
    mediaContainer.innerHTML += template.trim();
}

const downloadMedia = async (file_directory) => {
    axios.get(file_directory, { responseType: 'blob' })
        .then(response => {
            const extension = file_directory.split('.').pop();

            const mediaName = extension === 'mp4'
            ? `video.${extension}`
            :`image.${extension}`;

            const blob = new Blob([response.data], { type: response.headers['content-type'] });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = mediaName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error("Error fetching video:", error);
        });
}