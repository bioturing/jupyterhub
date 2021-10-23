import React from 'react';
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
    display_name
  } = props;


  return (
    <Card isCompact isExpanded key={key}>
        <CardTitle>
         
        </CardTitle>
        <CardHeader>
          <Flex direction={{ default: 'column' }}>
            <FlexItem>
              <Text>{category}</Text>
              <Text class="pf-u-font-weight-bold">{display_name}</Text>
            </FlexItem>
          </Flex>
         
        </CardHeader>
        <CardBody>
          <Flex direction={{ default: 'column' }} spaceItems={{ default: 'spaceItemsSm' }}>
            <FlexItem><Text>{description}</Text></FlexItem>
            <FlexItem><b>Tools</b> {tools.map(
                (name) => <Label variant="outline" color="grey" >
                {name}
              </Label>)}
            </FlexItem>
            
            <FlexItem><b>Format </b> 
                <Label variant="outline" color={fmtCode[format]} >
                  {format}
                </Label>
            </FlexItem>
            <FlexItem>
            <Button variant="link" style={{ '--pf-c-button--PaddingLeft': '0rem' }}>
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
    servers
  } = props;
  return (
    <Gallery hasGutter style={{ '--pf-l-gallery--GridTemplateColumns--min': '260px' }}>
     {servers.map((server, i) => {
       server.key = i;
       return NotebookCard(server)
     })} 
    </Gallery>
  );
};

NotebookCard.propTypes = {
    name: PropTypes.string,
    display_name: PropTypes.string,
    ready: PropTypes.bool,
    key: PropTypes.number, 
    user_options :PropTypes.object,
    category: PropTypes.string,
    description: PropTypes.string,
    tools: PropTypes.arrayOf(PropTypes.string),
    format: PropTypes.string,
}

NotebookCardList.propTypes = {
  servers: PropTypes.arrayOf(PropTypes.object)
}

export default NotebookCardList;