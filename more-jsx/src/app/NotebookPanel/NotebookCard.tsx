import React from 'react';
import { Link } from '@reach/router';

import {
  Card,
  CardTitle,
  CardBody,
  Gallery,
  Title,
  Text,
  Flex,
	FlexItem,
  Stack,
  Label,
  Chip,
  CardHeader
} from '@patternfly/react-core';

import ArrowRightIcon from '@patternfly/react-icons/dist/esm/icons/arrow-right-icon';
import { Button } from '@patternfly/react-core'; 
import PropTypes from 'prop-types';
import { useState } from 'react';
import { useEffect } from 'dist/main.bundle';

import {normalizeRoute} from '../../services/utils'
import { Redirect } from 'react-router-dom';


const fmtCode = {
    "IPython": "orange",
    "Rmd": "purple"
}  

const NotebookCard = (props) => {
  const {
    name,
    key,
    category,
    description,
    tools,
    format,
    display_name,
    id,
    user
  } = props;

  return (
    <Card isCompact isExpanded key={key}>
        <CardTitle>
         
        </CardTitle>
        <CardHeader>
          <Flex direction={{ default: 'column' }}>
            <FlexItem>
              <Text>{category}</Text>
              <Text className="pf-u-font-weight-bold">{display_name}</Text>
            </FlexItem>
          </Flex>
         
        </CardHeader>
        <CardBody>
          <Flex direction={{ default: 'column' }} spaceItems={{ default: 'spaceItemsSm' }}>
            <FlexItem><Text>{description}</Text></FlexItem>
            <FlexItem><b>Tools</b> {tools.map(
                (name, i) => <Label key={`$nb{id}-tool-${i}`} variant="outline" color="grey" style={{'margin-right': '0.2rem'}}>
                {name}
              </Label>)}
            </FlexItem>
            
            <FlexItem><b>Format </b> 
                <Label key={`$nb{id}-format`} variant="outline" color={fmtCode[format]} >
                  {format}
                </Label>
            </FlexItem>
            <FlexItem>
            <Button variant="link" 
                    style={{ '--pf-c-button--PaddingLeft': '0rem' }} 
                    component="a"
                    target="_blank"
                    href={normalizeRoute(`/notebook-spawn/${user}/${id}`)}
            >
              Open <ArrowRightIcon />
            </Button>
            </FlexItem>

          </Flex>
         
        </CardBody>
        
      </Card>
    )
  }

const NotebookCardList = (props) => {
  const {
    servers,
    user
  } = props;
  return (
    <Gallery hasGutter style={{ '--pf-l-gallery--GridTemplateColumns--min': '260px' }}>
     {servers.map((server, i) => {
       server.key = i;
       server.user = user;
       return NotebookCard(server)
     })} 
    </Gallery>
  );
};

NotebookCard.propTypes = {
    name: PropTypes.string,
    display_name: PropTypes.string,
    id: PropTypes.number,
    ready: PropTypes.bool,
    key: PropTypes.number, 
    user :PropTypes.string,
    category: PropTypes.string,
    description: PropTypes.string,
    tools: PropTypes.arrayOf(PropTypes.string),
    format: PropTypes.string,
}

NotebookCardList.propTypes = {
  servers: PropTypes.arrayOf(PropTypes.object),
  user: PropTypes.string
}

export default NotebookCardList;