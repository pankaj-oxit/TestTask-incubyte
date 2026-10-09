import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Link, Outlet, useLocation } from "react-router-dom";

export function Layout() {
  const location = useLocation();
  const tab = location.pathname.startsWith("/insights") ? "/insights" : "/employees";

  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}>
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            ACME Salary Manager
          </Typography>
        </Toolbar>
        <Tabs value={tab} textColor="inherit" indicatorColor="secondary" aria-label="Main navigation">
          <Tab label="Employees" value="/employees" component={Link} to="/employees" />
          <Tab label="Insights" value="/insights" component={Link} to="/insights" />
        </Tabs>
      </AppBar>
      <Container maxWidth="xl" sx={{ py: 3, flex: 1 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
