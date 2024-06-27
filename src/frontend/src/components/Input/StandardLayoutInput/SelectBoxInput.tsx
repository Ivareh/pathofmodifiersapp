import { Flex } from "@chakra-ui/layout";
import { HandleChangeEventFunction } from "../../../schemas/function/InputFunction";
import {
  AutoComplete,
  AutoCompleteInput,
  AutoCompleteItem,
  AutoCompleteList,
} from "@choc-ui/chakra-autocomplete";
import { FormControl, FormLabel } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { getEventTextContent } from "../../../hooks/utils";

export interface SelectBoxProps {
  optionsList: Array<SelectBoxOptionValue>;
  itemKeyId: string;
  defaultValue: string | undefined;
  defaultText: string | undefined;
  descriptionText?: string;
  getSelectTextValue: string;
  handleChange: HandleChangeEventFunction;
  width?: string | number;
  height?: string | number;
  staticPlaceholder?: string;
  centerInputText?: boolean;
  isDimmed?: boolean;
  noInputChange?: boolean;
  onFocusNotBlankInputText?: boolean;
  ml?: number | string;
  mr?: number | string;
}

export type SelectBoxOptionValue = { value: string | undefined; text: string };

export const SelectBoxInput = ({
  descriptionText,
  optionsList,
  itemKeyId,
  defaultValue,
  defaultText,
  getSelectTextValue,
  handleChange,
  width,
  height,
  staticPlaceholder,
  centerInputText,
  onFocusNotBlankInputText,
  isDimmed,
  noInputChange,
  ml,
  mr,
}: SelectBoxProps) => {
  defaultText = defaultText || "";
  const [inputText, setInputText] = useState<string>(defaultText);
  const [inputPlaceholder, setInputPlaceholder] = useState<string>(
    staticPlaceholder ? "" : defaultText
  );
  const [inputChanged, setInputChanged] = useState<boolean>(false);

  const optionValues = optionsList.map((option) =>
    option["text"].toLowerCase()
  );

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleChangeValue = (
    e: React.ChangeEvent<HTMLInputElement> | React.MouseEvent<HTMLElement>,
    actualValue?: string | undefined
  ) => {
    const target_value = getEventTextContent(e);
    setInputText(target_value);

    if (optionValues.includes(target_value.toLowerCase()) || !target_value) {
      if (!staticPlaceholder) {
        setInputPlaceholder(target_value);
      } else {
        setInputText("");
      }
      handleChange(e, actualValue);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      setInputText(defaultText || "");
    }
    if (getSelectTextValue !== "") {
      setInputText(getSelectTextValue);
    }
    if (
      getSelectTextValue !== defaultText &&
      getSelectTextValue !== "" &&
      getSelectTextValue !== undefined
    ) {
      setInputChanged(true);
    } else {
      setInputChanged(false);
    }
  }, [clearClicked, defaultText, getSelectTextValue]);

  return (
    <Flex
      marginTop={0}
      marginBottom={0}
      height={height}
      flexDirection={"row"}
      alignItems={"center"}
      width={width || "inputSizes.smallPPBox"}
    >
      <FormControl height={height || "lineHeights.tall"} color={"ui.white"}>
        {descriptionText && (
          <FormLabel color={"ui.white"} fontSize={15}>
            {descriptionText}
          </FormLabel>
        )}
        <AutoComplete
          openOnFocus
          listAllValuesOnFocus
          defaultValue={getSelectTextValue || defaultValue}
          emptyState={false}
        >
          <AutoCompleteInput
            value={inputText}
            onChange={(e) => handleChangeValue(e)}
            onFocus={() =>
              setInputText(onFocusNotBlankInputText ? inputPlaceholder : "")
            }
            pl={2}
            ml={ml || 0}
            mr={mr || 0}
            opacity={isDimmed ? 0.5 : 1.0}
            placeholder={
              staticPlaceholder ? staticPlaceholder : inputPlaceholder
            }
            focusBorderColor="ui.white"
            borderRadius={inputPlaceholder !== defaultText ? 9 : 6}
            borderWidth={inputPlaceholder !== defaultText ? 2 : 1}
            borderColor={
              inputChanged && !noInputChange ? "ui.inputChanged" : "ui.grey"
            }
            textAlign={centerInputText ? "center" : "left"}
            fontSize={16}
            bgColor={"ui.input"}
            autoComplete="off"
          />
          <AutoCompleteList
            onBlur={() =>
              setInputText(staticPlaceholder ? "" : inputPlaceholder)
            }
            borderColor={"ui.grey"}
            bgColor="ui.input"
            margin={0}
            p={0}
            marginBottom={0}
            maxH={"200px"}
            overflowY={"auto"}
          >
            {optionsList.map((option) => (
              <AutoCompleteItem
                value={option["text"]}
                key={descriptionText + itemKeyId + option["value"]}
                style={{
                  color: "white",
                  backgroundColor: "#2d3333",
                  margin: 0,
                  borderRadius: 0,
                }}
                onClick={(e) => handleChangeValue(e, option["value"])}
              >
                {option["text"]}
              </AutoCompleteItem>
            ))}
          </AutoCompleteList>
        </AutoComplete>
      </FormControl>
    </Flex>
  );
};
