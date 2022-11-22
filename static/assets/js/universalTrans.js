// access microphone to get input from user
// const player = document.getElementById('player');

// const handleSuccess = function (stream) {
//   if (window.URL) {
//     player.srcObject = stream;
//   } else {
//     player.src = stream;
//   }
// };

// navigator.mediaDevices
//   .getUserMedia({audio: true, video: false})
//   .then(handleSuccess);


// Stop and save data from the microphone
const startButton = document.getElementById('start');
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');


const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  // Event starts recording
  startButton.addEventListener('click', function() {
    mediaRecorder.start();
  });

  // Event makes sure that download is not empty
  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) recordedChunks.push(e.data);
  });

  // Event saves + downloads file
  mediaRecorder.addEventListener('stop', function() {
    downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    downloadLink.download = 'recordedAudio.wav';
  });

  // Event stops recording
  stopButton.addEventListener('click', function() {
    mediaRecorder.stop();
  });

//   mediaRecorder.start();
};
// only want audio, not webcam
navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);