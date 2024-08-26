import express from "express";
const router = express.Router();

router.get("/", async function (req, res, next) {
  const ipLocation = await fetch("http://ip-api.com/json/")
    .then((res) => res.json())
    .catch(() => ({ status: "fail" }));

  if (ipLocation.status === "fail") {
    return `Hello! Failed to get the server location :(`;
  }

  const formattedTime = new Date().toLocaleString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });

  res.send({
    message: `Hello! This response was served from ${ipLocation.city}, ${ipLocation.country} (${ipLocation.lat}, ${ipLocation.lon}) at ${formattedTime}`,
  });
});

router.get("/:nr", async function (req, res, next) {
  const nr = req.params.nr;
  if (nr % 2 === 1) {
    return res.status(404).send("Not Found");
  }
  if (nr % 2 === 0) res.send(req.params.nr);
});

router.get("/timeout/:nr", async function (req, res, next) {
  const nr = req.params.nr;
  if (nr % 2 === 0) {
    return;
  }
  res.send(req.params.nr);
});

router.get("/error/:nr", async function (req, res, next) {
  const nr = req.params.nr;
  if (nr % 3 === 0) {
    throw new Error("Error occurred");
  }
  res.send(nr);
});
export default router;
