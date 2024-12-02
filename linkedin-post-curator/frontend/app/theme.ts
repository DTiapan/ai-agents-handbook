import { extendTheme } from "@chakra-ui/react";

export const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: "gray.50",
      },
    },
  },
  components: {
    Button: {
      defaultProps: {
        size: "md",
      },
      variants: {
        solid: {
          display: "flex",
          gap: "2",
          alignItems: "center",
        },
        outline: {
          display: "flex",
          gap: "2",
          alignItems: "center",
        },
      },
    },
  },
});
