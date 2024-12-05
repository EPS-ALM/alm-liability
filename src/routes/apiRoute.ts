import { Router } from 'express';

const router = Router();

router.get("/", (req, res) =>
  res.send("Bem vindo ao XXXXXXXXXXXXXXXXXXXXXXXXX")
);
/* router.use("/auth", authRoute); */

export default router;
