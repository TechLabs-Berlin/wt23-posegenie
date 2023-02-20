import * as React from "react";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";

export default function Header() {
  return (
    <Box>
      <Paper elevation={10} className="header">
        <div className="header_element">
          <span className="material-symbols-outlined">image</span>
        </div>
        <div className="header_element">
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry's standard dummy text ever
          since the 1500s, when an unknown printer took a galley of type and
          scrambled it to make a type specimen book. It has survived not only
          five centuries, but also the leap into electronic typesetting,
          remaining essentially unchanged.
        </div>
      </Paper>
    </Box>
  );
}
