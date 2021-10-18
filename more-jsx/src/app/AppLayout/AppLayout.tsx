import * as React from 'react';
import { NavLink, useLocation, useHistory } from 'react-router-dom';
import {
  Nav,
  NavList,
  NavItem,
  Page,
  PageHeader,
  SkipToContent
} from '@patternfly/react-core';
import { routes, IAppRoute} from '@app/routes';
import logo from '@app/bgimages/bioturing-jupyter.svg';

interface IAppLayout {
  children: React.ReactNode;
}

const AppLayout: React.FunctionComponent<IAppLayout> = ({ children }) => {
  const [isNavOpen, setIsNavOpen] = React.useState(true);
  const [isMobileView, setIsMobileView] = React.useState(true);
  const [isNavOpenMobile, setIsNavOpenMobile] = React.useState(false);
  const [activeItem, setActiveItem] = React.useState(0); 

  const onNavSelect = (result) => {
    setActiveItem(result.itemId);
  };
 
  const onPageResize = (props: { mobileView: boolean; windowSize: number }) => {
    setIsMobileView(props.mobileView);
  };

  function LogoImg() {
    const history = useHistory();
    function handleClick() {
      history.push('/');
    }
    return (
      <img src={logo} onClick={handleClick} alt="BioTuring Logo" />
    );
  }

  const Header = (
    <PageHeader
      logo={<LogoImg />}
    />
  );

  const location = useLocation();

  const renderNavItem = (route: IAppRoute, index: number) => (
    <NavItem key={`${route.label}-${index}`} id={`${route.label}-${index}`}>
      <NavLink exact={route.exact} to={route.path} activeClassName="pf-m-current">
        {route.label}
      </NavLink>
    </NavItem>
  )
  const PageNav = (
    <Nav id="nav-primary-simple" variant="tertiary" onSelect={onNavSelect} aria-label="Nav">
      <NavList id="nav-list-simple" >
        {routes.map((route, idx) => {
          if (!route.hideFromNav)
            return renderNavItem(route, idx)
          else
            return null
          })}
      </NavList>
    </Nav>
  );

  const pageId = 'primary-app-container';

  const PageSkipToContent = (
    <SkipToContent onClick={(event) => {
      event.preventDefault();
      const primaryContentContainer = document.getElementById(pageId);
      primaryContentContainer && primaryContentContainer.focus();
    }} href={`#${pageId}`}>
      Skip to Content
    </SkipToContent>
  );
  return (
    <Page
      mainContainerId={pageId}
      header={Header}
      onPageResize={onPageResize}
      tertiaryNav={PageNav}
      skipToContent={PageSkipToContent}>
      {children}
    </Page>
  );
}

export { AppLayout };
