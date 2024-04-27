import { Html, Head, Main, NextScript, DocumentContext } from "next/document";
import {
  DocumentHeadTags,
  DocumentHeadTagsProps,
  documentGetInitialProps,
  AppCacheProvider,
} from "@mui/material-nextjs/v13-pagesRouter";
import { JSX } from "react";
export default function Document(
  props: JSX.IntrinsicAttributes & DocumentHeadTagsProps
) {
  return (
    <Html>
      <AppCacheProvider {...props}>
        <Head>
          <DocumentHeadTags {...props} />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </AppCacheProvider>
    </Html>
  );
}

Document.getInitialProps = async (ctx: DocumentContext) => {
  const finalProps = await documentGetInitialProps(ctx);
  return finalProps;
};
