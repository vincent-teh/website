var socket = io.connect(
	window.location.protocol + "//" + document.domain + ":" + location.port
);

socket.on("connect", function () {
	console.log("Connected...!", socket.connected);
});

socket.on("processed_image", function (image) {
	photo.setAttribute("src", image);
});

const FPS = 10;
setInterval(() => {
	socket.emit("image", 0);
}, 1000 / FPS);

