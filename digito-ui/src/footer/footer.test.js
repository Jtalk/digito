import React from 'react';
import * as Enzyme from "enzyme";
import {mount, shallow} from "enzyme";
import Adapter from 'enzyme-adapter-react-16';

import Footer from "./footer";
import FlatLinksList from "./flat-links-list";
import FlatLogoList from "./flat-logo-list";
import {Container, Segment} from "semantic-ui-react";

Enzyme.configure({ adapter: new Adapter() });

describe("<Footer/>", () => {
  let links = [
    {name: "Link1", href: "/test/link1"},
    {name: "Link2", href: "test/link2"},
    {name: "Link3", href: "test/link3"}
  ];
  let logos = [
    {
      href: "/test/logo-link1",
      src: "/test/images/logo1.svg",
      name: "Test Logo 1",
      height: 55
    },
    {
      href: "/test/logo-link2",
      src: "/test/images/logo2.jpg",
      name: "Test Logo 2",
      height: 40
    }
  ];
  it('renders without errors', () => {
    mount(<Footer links={links} logos={logos}/>);
  });
  it('renders without links or logos', () => {
    mount(<Footer links={[]} logos={[]}/>);
  });
  it('forwards links and logos to proper children', () => {
    let result = shallow(<Footer links={links} logos={logos}/>);
    expect(result.find(FlatLinksList).props()).toMatchObject({links: links});
    expect(result.find(FlatLogoList).props()).toMatchObject({logos: logos});
  });
  it('renders centrally aligned', () => {
    let result = shallow(<Footer links={links} logos={logos}/>);
    // I've got absolutely no idea how to test it more appropriately
    expect(result.findWhere(n => n.is(Container) && n.props().textAlign !== "center").getElements().length).toBe(0);
    expect(result.findWhere(n => n.is(Segment) && n.props().textAlign !== "center").getElements().length).toBe(0);
  });
});
