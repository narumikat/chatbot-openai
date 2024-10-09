$(document).ready(function () {
    $('#record-btn').click(function () {
        $('#status').text('Recording audio...');
        $.ajax({
            url: '/send',
            type: 'POST',
            success: function (data) {
                $('#status').text('Recording completed!');

                setTimeout(function () {
                    $('#status').text('Record new audio');
                }, 3000);

                // Add user message
                $('#chat-history').append(`
                    <div class="d-flex align-items-center justify-content-end">
                        <div class="user-msg">
                            <p>${data.transcription}</p>
                        </div>
                        <img src="${userPhotoUrl}" alt="Avatar" class="avatar ms-2">
                    </div>
                `);

                // Add ChatGPT answer
                $('#chat-history').append(`
                    <div class="d-flex align-items-center justify-content-start">
                        <img src="${chatGptLogoUrl}" alt="Avatar" class="avatar me-2">
                        <div class="chatgpt-msg">
                            <p>${data.chatgpt_response}</p>
                        </div>
                    </div>
                `);

                const audioElement = document.getElementById('audio-response');
                audioElement.src = data.audio_file; // Update to new audio file
                audioElement.load();
                audioElement.playbackRate = 1.8;
                audioElement.play();

                $('#chat-history').animate({scrollTop: $('#chat-history')[0].scrollHeight}, 500);
            },
        });
    });
});
