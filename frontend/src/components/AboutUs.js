import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import teamPic from "../assets/img_001.jpg";

export default function AboutUs() {
  return (
    <Card className="card_Aboutus" sx={{ maxWidth: 645 }}>
      {/* <img src={teamPic} alt="team" className="team_img" /> */}

      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          About us
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry's standard dummy text ever
          since the
        </Typography>
      </CardContent>
      <CardActions>
        <a>
          <Button size="small" color="secondary">
            Share
          </Button>
        </a>
        <a href="https://bln.techlabs.org/">
          <Button size="small">Learn More</Button>
        </a>
      </CardActions>
    </Card>
  );
}
