import React from 'react';
import * as Enzyme from "enzyme";
import {mount} from "enzyme";
import Adapter from 'enzyme-adapter-react-16';

import FlatLinksList from "./flat-links-list";
import VerticalSeparator from "./vertical-separator";
import FlatLogoList from "./flat-logo-list";

Enzyme.configure({ adapter: new Adapter() });

describe("<FlatLogoList/>", () => {
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
  it('renders empty list', () => {
    mount(<FlatLogoList logos={[]}/>);
  });
  it('renders empty list with spacing', () => {
    mount(<FlatLogoList logos={[]} spacing="50px"/>);
  });
  it('renders single logo without spacing', () => {
    let result = mount(<FlatLogoList logos={[logos[0]]} spacing="50px"/>);
    expect(result.find("a").props().style).toEqual({});
    expect(result.find("a").props()).toMatchObject({href: logos[0].href});
    expect(result.find("a").find("img").props()).toMatchObject({src: logos[0].src, alt: logos[0].name, height: logos[0].height})
  });
  it('renders multiple logos with spacing', () => {
    let result = mount(<FlatLogoList logos={logos} spacing="50px"/>);
    expect(result.find("a").filter({href: logos[0].href}).props().style).toEqual({});
    expect(result.find("a").filter({href: logos[1].href}).props().style).toEqual({marginLeft: "50px !important"});
    expect(result.find("a").filter({href: logos[0].href}).find("img").props()).toMatchObject({src: logos[0].src, alt: logos[0].name, height: logos[0].height});
    expect(result.find("a").filter({href: logos[0].href}).find("img").props()).toMatchObject({src: logos[0].src, alt: logos[0].name, height: logos[0].height});
  });
  it('renders multiple logos without spacing', () => {
    let result = mount(<FlatLogoList logos={logos}/>);
    expect(result.find("a").filter({href: logos[0].href}).props().style).toEqual({});
    expect(result.find("a").filter({href: logos[1].href}).props().style).toEqual({});
    expect(result.find("a").filter({href: logos[0].href}).find("img").props()).toMatchObject({src: logos[0].src, alt: logos[0].name, height: logos[0].height});
    expect(result.find("a").filter({href: logos[0].href}).find("img").props()).toMatchObject({src: logos[0].src, alt: logos[0].name, height: logos[0].height});
  });
});
