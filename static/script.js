document.addEventListener("DOMContentLoaded", () => {
    const startWebcamBtn = document.getElementById("start-webcam");
    const uploadVideoBtn = document.getElementById("upload-video");
    const stopStreamBtn = document.getElementById("stop-stream");
    const videoInput = document.getElementById("video-input");

    startWebcamBtn.addEventListener("click", (e) => {
        e.preventDefault();
        fetch("/start_webcam", { method: "POST" })
            .then(() => {

                const videoFeed = document.getElementById("video-feed");
                videoFeed.src = "/video_feed";
            })
            .catch((error) => console.error("Error starting webcam:", error));
    });

    uploadVideoBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const formData = new FormData();
    const file = videoInput.files[0];
    if (file) {
        formData.append("video", file);


        fetch("/reset_feed", { method: "POST" })
            .then(() => {

                fetch("/upload_video", {
                    method: "POST",
                    body: formData,
                })
                    .then(() => {
                        const videoFeed = document.getElementById("video-feed");

                        videoFeed.src = "";
                        setTimeout(() => {
                            videoFeed.src = "/video_feed";
                        }, 100);
                    })
                    .catch((error) => console.error("Error uploading video:", error));
            })
            .catch((error) => console.error("Error resetting feed:", error));
    } else {
        alert("Please select a video to upload.");
    }
});


    stopStreamBtn.addEventListener("click", (e) => {
        e.preventDefault();
        fetch("/stop_stream", { method: "POST" })
            .then(() => {
                const videoFeed = document.getElementById("video-feed");
                videoFeed.src = ""; //
            })
            .catch((error) => console.error("Error stopping stream:", error));
    });
})