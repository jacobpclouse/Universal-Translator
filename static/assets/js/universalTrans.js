// send to server  
const sendAudioFile = file => {
  const formData = new FormData();
  formData.append('audio-file', file);
  return fetch('http://localhost:5000/audioUpload', {
    mode: 'no-cors',
    method: 'POST',
    body: formData
  });
};


// Stop and save data from the microphone
const startButton = document.getElementById('start');
const downloadLink = document.getElementById('download');
const stopButton = document.getElementById('stop');


const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];  // this is where audio data will be stored -- can be made into a blob
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
    downloadLink.download = 'microphoneAudio.mp3';

//   // Create a Blob when recording has stopped.
      // recorder.addEventListener('stop', () => {
      const blob = new Blob(recordedChunks, { 
        'type': 'audio/mp3' 
        });
        sendAudioFile(blob);
      // });



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


// // ----------------------------------
// navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
//   // Collection for recorded data.
//   let data = [];

//   // Recorder instance using the stream.
//   // Also set the stream as the src for the audio element.
//   const recorder = new MediaRecorder(stream);
//   audio.srcObject = stream;

//   recorder.addEventListener('start', e => {
//     // Empty the collection when starting recording.
//     data.length = 0;
//   });

//   recorder.addEventListener('dataavailable', event => {
//     // Push recorded data to collection.
//     data.push(event.data);
//   });

//   // Create a Blob when recording has stopped.
//   recorder.addEventListener('stop', () => {
//     const blob = new Blob(data, { 
//       'type': 'audio/mp3' 
//     });
//     sendAudioFile(blob);
//   });

//   // Start the recording.
//   recorder.start();
// });